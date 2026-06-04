from django.contrib import admin
from .models import Prediction
from apps.leagues.models import League
class PredictionLeagueFilter(admin.SimpleListFilter):
    """Filtro personalizado para ver predicciones por Liga en la barra lateral."""
    title = 'Liga'
    parameter_name = 'league_id'

    def lookups(self, request, model_admin):
        # Trae todas las ligas disponibles para listar en la barra derecha
        return League.objects.all().values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            # Filtra las predicciones de los usuarios que están anotados en la liga seleccionada.
            # (Ajustá 'user__leagues__id' si la relación ManyToMany en tu modelo League se llama distinto)
            return queryset.filter(user__leagues__id=self.value())
        return queryset
@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'prediction_display', 'points', 'is_exact', 'is_winner', 'created_at')
    list_filter = (PredictionLeagueFilter,'is_exact', 'is_winner', 'created_at', 'match__status')
    search_fields = ('user__username', 'match__home_team__name', 'match__away_team__name')
    readonly_fields = ('points', 'is_exact', 'is_winner', 'created_at', 'updated_at')
    ordering = ('-created_at',)

    fieldsets = (
        ('Información', {
            'fields': ('user', 'match', 'created_at', 'updated_at')
        }),
        ('Predicción', {
            'fields': ('home_goals', 'away_goals')
        }),
        ('Resultados', {
            'fields': ('points', 'is_exact', 'is_winner'),
            'classes': ('collapse',)
        }),
    )

    def prediction_display(self, obj):
        return f"{obj.home_goals} - {obj.away_goals}"
    prediction_display.short_description = 'Predicción'

    def match_result_display(self, obj):
        match = obj.match
        # Ajustá 'home_score'/'away_score' según cómo se llamen los goles reales en tu modelo Match
        if hasattr(match, 'home_goals') and match.home_goals is not None:
            return f"{match.home_goals} - {match.away_goals}"
        elif hasattr(match, 'home_score') and match.home_score is not None:
            return f"{match.home_score} - {match.away_score}"
        return "Pendiente"
    match_result_display.short_description = 'Resultado Real'

    def get_queryset(self, request):
        """Optimiza la consulta para que el admin vuele y no consuma RAM en el VPS."""
        return super().get_queryset(request).select_related('user', 'match')