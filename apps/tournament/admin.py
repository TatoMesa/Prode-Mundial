from django.contrib import admin
from .models import Group, GroupStanding, KnockoutRound, KnockoutMatch
from .services import recalculate_group_standings


class GroupStandingInline(admin.TabularInline):
    model = GroupStanding
    extra = 0
    fields = ('team', 'played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'points')


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_list')
    filter_horizontal = ('teams',)
    inlines = (GroupStandingInline,)
    actions = ('recalculate_standings',)

    def team_list(self, obj):
        return ', '.join(t.name for t in obj.teams.all())
    team_list.short_description = 'Equipos'

    def recalculate_standings(self, request, queryset):
        for group in queryset:
            recalculate_group_standings(group)
        self.message_user(request, f'Tabla recalculada para {queryset.count()} grupo(s).')
    recalculate_standings.short_description = 'Recalcular tabla de posiciones'


@admin.register(GroupStanding)
class GroupStandingAdmin(admin.ModelAdmin):
    list_display = ('group', 'team', 'played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'points')
    list_editable = ('played', 'won', 'drawn', 'lost', 'goals_for', 'goals_against', 'points')
    list_filter = ('group',)


@admin.register(KnockoutRound)
class KnockoutRoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


@admin.register(KnockoutMatch)
class KnockoutMatchAdmin(admin.ModelAdmin):
    list_display = ('round', 'slot_number', 'match', 'slot_home', 'slot_away', 'went_to_penalties')
    list_editable = ('slot_number',)
    list_filter = ('round',)
    ordering = ('round__order', 'slot_number')
    fields = (
        'round', 'match', 'slot_number', 'slot_home', 'slot_away',
        'went_to_penalties', 'home_penalties', 'away_penalties',
    )