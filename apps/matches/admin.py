from django.contrib import admin
from django.utils.html import format_html
from .models import Team, Match


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('flag', 'name', 'code')
    search_fields = ('name', 'code')


class MatchStatusFilter(admin.SimpleListFilter):
    title = 'Estado'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return Match.Status.choices

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status=self.value())
        return queryset


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = (
        'home_team', 'away_team', 'kickoff_time',
        'score_display', 'status_badge'
    )
    list_filter = (MatchStatusFilter,)
    search_fields = ('home_team__name', 'away_team__name')
    list_editable = ('home_score', 'away_score', 'status')  # Solo en list_display también
    readonly_fields = ()
    fields = (
        'home_team', 'away_team', 'kickoff_time',
        'home_score', 'away_score', 'status'
    )

    # Sobrescribir list_display para incluir los campos editables
    list_display = (
        'home_team', 'away_team', 'kickoff_time',
        'home_score', 'away_score', 'status', 'score_display'
    )
    list_editable = ('home_score', 'away_score', 'status')

    def score_display(self, obj):
        if obj.home_score is not None:
            return format_html(
                '<strong>{} - {}</strong>',
                obj.home_score, obj.away_score
            )
        return '—'
    score_display.short_description = 'Resultado'

    def status_badge(self, obj):
        colors = {
            'PENDING': 'secondary',
            'IN_PROGRESS': 'warning',
            'FINISHED': 'success',
        }
        color = colors.get(obj.status, 'secondary')
        return format_html(
            '<span class="badge bg-{}">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Estado'
    status_badge.allow_tags = True