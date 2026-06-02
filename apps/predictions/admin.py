from django.contrib import admin
from .models import Prediction


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('user', 'match', 'prediction_display', 'points', 'is_exact', 'is_winner', 'created_at')
    list_filter = ('is_exact', 'is_winner', 'created_at', 'match__status')
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
