# apps/matches/views.py
from django.views.generic import ListView, DetailView
from django.db.models import Case, When, IntegerField
from .models import Match


class MatchListView(ListView):
    model = Match
    template_name = 'matches/list.html'
    context_object_name = 'matches'

    def get_queryset(self):
        estado = self.request.GET.get('estado')

        if estado in ('PENDING', 'IN_PROGRESS', 'FINISHED'):
            return Match.objects.select_related('home_team', 'away_team').filter(
                status=estado
            ).order_by('kickoff_time')

        if estado == 'todos':
            return Match.objects.select_related('home_team', 'away_team').order_by('kickoff_time')

        # Por defecto: en juego primero, luego pendientes — sin finalizados
        return Match.objects.select_related('home_team', 'away_team').exclude(
            status=Match.Status.FINISHED
        ).annotate(
            order=Case(
                When(status=Match.Status.IN_PROGRESS, then=0),
                When(status=Match.Status.PENDING, then=1),
                default=2,
                output_field=IntegerField(),
            )
        ).order_by('order', 'kickoff_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            from apps.predictions.models import Prediction
            predictions = Prediction.objects.filter(user=self.request.user)
            context['predicted_ids'] = set(
                predictions.values_list('match_id', flat=True)
            )
            context['predictions_map'] = {p.match_id: p for p in predictions}
        else:
            context['predicted_ids'] = set()
            context['predictions_map'] = {}
        return context


class MatchDetailView(DetailView):
    model = Match
    template_name = 'matches/detail.html'
    context_object_name = 'match'

    def get_queryset(self):
        return Match.objects.select_related('home_team', 'away_team')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            from apps.predictions.models import Prediction
            context['user_prediction'] = (
                Prediction.objects
                .filter(user=self.request.user, match=self.object)
                .first()
            )
        else:
            context['user_prediction'] = None
        return context