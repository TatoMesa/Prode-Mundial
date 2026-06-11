# apps/leagues/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import FormView, DetailView, ListView
from django.urls import reverse_lazy
from django.db.models import Sum, Count, Q
from django.contrib.auth.models import User

from .models import League, LeagueMembership
from .forms import JoinLeagueForm
from django.db.models import Sum, Count, Q, F


class JoinLeagueView(LoginRequiredMixin, FormView):
    """El usuario ingresa el código para unirse a una liga."""
    template_name = 'leagues/join.html'
    form_class = JoinLeagueForm
    success_url = reverse_lazy('leagues:my_leagues')

    def form_valid(self, form):
        code = form.cleaned_data['code']
        league = League.objects.get(code=code)

        _, created = LeagueMembership.objects.get_or_create(
            user=self.request.user,
            league=league,
        )
        if created:
            messages.success(self.request, f'¡Te uniste a la liga "{league.name}"!')
        else:
            messages.info(self.request, f'Ya sos miembro de la liga "{league.name}".')
        return super().form_valid(form)


class MyLeaguesView(LoginRequiredMixin, ListView):
    """Lista de ligas a las que pertenece el usuario."""
    template_name = 'leagues/my_leagues.html'
    context_object_name = 'leagues'

    def get_queryset(self):
        return League.objects.filter(
            members=self.request.user,
            is_active=True,
        )


class LeagueRankingView(LoginRequiredMixin, DetailView):
    """Ranking de una liga privada — solo visible para sus miembros."""
    model = League
    template_name = 'leagues/ranking.html'
    context_object_name = 'league'
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def dispatch(self, request, *args, **kwargs):
        league = self.get_object()
        # Solo los miembros pueden ver el ranking
        if not league.members.filter(pk=request.user.pk).exists():
            messages.error(request, 'No sos miembro de esta liga.')
            return redirect('leagues:join')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        league = self.get_object()

        # Ranking de los miembros de esta liga
        context['ranking'] = (
            User.objects
            .filter(memberships__league=league)
            .annotate(
                total_points=Sum('predictions__points'),
                exact_count=Count('predictions__id', filter=Q(predictions__is_exact=True)),
                winner_count=Count('predictions__id', filter=Q(predictions__is_winner=True)),
            )
            F('total_points').desc(nulls_last=True),
            F('exact_count').desc(nulls_last=True),
            'username',
        )
        return context