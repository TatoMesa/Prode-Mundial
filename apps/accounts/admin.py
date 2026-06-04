from django.contrib import admin
from .models import UserProfile
from django.db.models import Prefetch
from apps.predictions.models import Prediction
from apps.leagues.models import League
 
class LeagueFilter(admin.SimpleListFilter):
    title = 'Liga'  # El título que se verá sobre el filtro lateral
    parameter_name = 'league_id'  # El parámetro que se pasará en la URL

    def lookups(self, request, model_admin):
        """Define las opciones que aparecen en la barra lateral."""
        # Trae todas las ligas disponibles para listar en el filtro
        leagues = League.objects.all().values_list('id', 'name')
        return [(league[0], league[1]) for league in leagues]

    def queryset(self, request, queryset):
        """Aplica el filtro a la lista de perfiles."""
        if self.value():
            # Filtramos los perfiles cuyos usuarios pertenezcan a la liga seleccionada
            # (Ajustá 'users' o el related_name según cómo esté tu relación ManyToMany en League)
            return queryset.filter(user__leagues__id=self.value()).distinct()
        return queryset 
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')
    list_filter = (LeagueFilter, 'created_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('created_at',)
    def get_queryset(self, request):
        """Optimiza la consulta para traer los pronósticos de un tirón (Evita el problema N+1)."""
        queryset = super().get_queryset(request)
        # Usamos Prefetch para traernos todos los pronósticos de cada usuario eficientemente
        return queryset.select_related('user').prefetch_related(
            Prefetch('user__predictions', queryset=Prediction.objects.all(), to_attr='cached_predictions')
        )

    def ver_pronosticos_count(self, obj):
        """Muestra la cantidad de pronósticos cargados por el usuario en la lista."""
        # Como usamos 'to_attr' en el prefetch, podemos contar desde la memoria RAM sin hacer más consultas a la base de datos
        return len(getattr(obj.user, 'cached_predictions', []))
    
    ver_pronosticos_count.short_description = 'Pronósticos Totales'
 
    def ver_pronosticos_detalle(self, obj):
        """Dibuja los pronósticos reales de este usuario en la celda."""
        predictions = getattr(obj.user, 'cached_predictions', [])
        if not predictions:
            return "-"
        
        # Armamos una lista de texto con los pronósticos que hizo
        # Ajustá 'prediction.home_score', 'prediction.away_score' o como tengas tus campos
        lineas = []
        for p in predictions[:5]:  # Limitamos a los primeros 5 para que no explote la pantalla
            # Ejemplo: "Argentina vs Francia: 2-1"
            lineas.append(f"{p.match}: {p.home_score}-{p.away_score}")
            
        if len(predictions) > 5:
            lineas.append("...")
            
        return ", ".join(lineas)
    ver_pronosticos_detalle.short_description = 'Últimos Pronósticos'