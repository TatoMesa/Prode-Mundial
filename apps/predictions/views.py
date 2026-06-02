# apps/predictions/views.py
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Q

from apps.matches.models import Match
from apps.predictions.models import Prediction
from apps.predictions.scoring import calculate_points


class PredictionCreateUpdateView(LoginRequiredMixin, CreateView):
    """Vista para crear o actualizar una predicción de un partido."""
    model = Prediction
    fields = ('home_goals', 'away_goals')
    template_name = 'predictions/prediction_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.match = Match.objects.get(pk=kwargs['match_pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'] = self.match
        context['is_locked'] = self.match.is_locked
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        try:
            existing = Prediction.objects.get(user=self.request.user, match=self.match)
            form.instance = existing
            form.initial = {
                'home_goals': existing.home_goals,
                'away_goals': existing.away_goals,
            }
        except Prediction.DoesNotExist:
            pass
        return form

    def get_object(self, queryset=None):
        try:
            return Prediction.objects.get(user=self.request.user, match=self.match)
        except Prediction.DoesNotExist:
            return None

    def form_valid(self, form):
        if self.match.is_locked:
            messages.error(self.request, 'Este partido ya está bloqueado para predicciones.')
            return redirect('matches:detail', pk=self.match.pk)

        prediction = form.save(commit=False)
        prediction.user = self.request.user
        prediction.match = self.match

        if self.match.status == Match.Status.FINISHED:
            prediction.points, prediction.is_exact, prediction.is_winner = calculate_points(
                self.match.home_score, self.match.away_score,
                prediction.home_goals, prediction.away_goals,
            )

        prediction.save()
        messages.success(self.request, '¡Predicción guardada exitosamente!')
        return redirect('matches:list')

    def get_success_url(self):
        return reverse_lazy('matches:list')


class UserPredictionsListView(LoginRequiredMixin, ListView):
    """Lista de predicciones del usuario autenticado."""
    model = Prediction
    template_name = 'predictions/user_predictions_list.html'
    context_object_name = 'predictions'
    paginate_by = 20

    def get_queryset(self):
        return Prediction.objects.filter(
            user=self.request.user
        ).select_related('match', 'match__home_team', 'match__away_team').order_by('match__kickoff_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        predictions = self.get_queryset()
        context['stats'] = {
            'total': predictions.count(),
            'total_points': predictions.aggregate(Sum('points'))['points__sum'] or 0,
            'exact_count': predictions.filter(is_exact=True).count(),
            'winner_count': predictions.filter(is_winner=True, is_exact=False).count(),
        }
        return context


class RankingView(ListView):
    """Ranking de usuarios por puntos totales acumulados."""
    model = Prediction
    template_name = 'predictions/ranking.html'
    context_object_name = 'ranking'
    paginate_by = 50

    def get_queryset(self):
        from django.contrib.auth.models import User
        return User.objects.annotate(
            total_points=Sum('predictions__points'),
            prediction_count=Count('predictions', filter=Q(predictions__isnull=False)),
            exact_count=Count('predictions', filter=Q(predictions__is_exact=True)),
            winner_count=Count('predictions', filter=Q(predictions__is_winner=True, predictions__is_exact=False)),
        ).filter(
            prediction_count__gt=0
        ).order_by('-total_points', '-exact_count', 'username')


class PredictionDetailView(LoginRequiredMixin, DetailView):
    """Detalle de una predicción específica del usuario."""
    model = Prediction
    template_name = 'predictions/prediction_detail.html'
    context_object_name = 'prediction'

    def get_queryset(self):
        return Prediction.objects.filter(
            user=self.request.user
        ).select_related('match', 'match__home_team', 'match__away_team')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        prediction = self.get_object()
        if prediction.match.status == Match.Status.FINISHED:
            context['result_home'] = prediction.match.home_score
            context['result_away'] = prediction.match.away_score
            context['is_finished'] = True
        return context
    
class PredictionEditView(LoginRequiredMixin, UpdateView):
    """Editar una predicción existente por su pk."""
    model = Prediction
    fields = ('home_goals', 'away_goals')
    template_name = 'predictions/prediction_form.html'

    def get_queryset(self):
        # Solo puede editar sus propias predicciones
        return Prediction.objects.filter(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        prediction = self.get_object()
        if prediction.match.is_locked:
            messages.error(request, 'Este partido ya está bloqueado para predicciones.')
            return redirect('matches:list')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['match'] = self.get_object().match
        return context

    def form_valid(self, form):
        messages.success(self.request, '¡Predicción actualizada exitosamente!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('matches:list')