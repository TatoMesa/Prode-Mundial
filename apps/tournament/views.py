from django.views.generic import TemplateView
from .models import Group, KnockoutRound


class GroupStandingsView(TemplateView):
    template_name = 'tournament/groups.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.prefetch_related(
            'standings__team', 'teams'
        ).order_by('name')
        return context


class KnockoutView(TemplateView):
    template_name = 'tournament/knockout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rounds'] = KnockoutRound.objects.prefetch_related(
            'matches__match__home_team',
            'matches__match__away_team',
        ).order_by('order')
        return context