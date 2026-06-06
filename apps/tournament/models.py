from django.db import models
from apps.matches.models import Team, Match


class Group(models.Model):
    """Grupo de la fase de grupos (A, B, C...)."""
    name = models.CharField(max_length=10, verbose_name='Nombre')  # "A", "B"...
    teams = models.ManyToManyField(Team, related_name='groups', verbose_name='Equipos')

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']

    def __str__(self):
        return f'Grupo {self.name}'


class GroupStanding(models.Model):
    """
    Tabla de posiciones de un equipo dentro de un grupo.
    Se recalcula automáticamente vía señal post_save en Match.
    También editable desde el admin para correcciones manuales.
    """
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='standings', verbose_name='Grupo')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='standings', verbose_name='Equipo')
    played = models.PositiveSmallIntegerField(default=0, verbose_name='PJ')
    won = models.PositiveSmallIntegerField(default=0, verbose_name='G')
    drawn = models.PositiveSmallIntegerField(default=0, verbose_name='E')
    lost = models.PositiveSmallIntegerField(default=0, verbose_name='P')
    goals_for = models.PositiveSmallIntegerField(default=0, verbose_name='GF')
    goals_against = models.PositiveSmallIntegerField(default=0, verbose_name='GC')
    points = models.PositiveSmallIntegerField(default=0, verbose_name='Pts')

    class Meta:
        verbose_name = 'Posición'
        verbose_name_plural = 'Tabla de posiciones'
        unique_together = ('group', 'team')
        ordering = ['-points', '-won', 'goals_against']

    def __str__(self):
        return f'{self.group} — {self.team}: {self.points} pts'

    @property
    def goal_difference(self):
        return self.goals_for - self.goals_against


class KnockoutRound(models.Model):
    """Fase eliminatoria: Dieciseisavos, Octavos, Cuartos, Semis, Final."""
    name = models.CharField(max_length=50, verbose_name='Nombre')
    order = models.PositiveSmallIntegerField(verbose_name='Orden', help_text='1=Dieciseisavos, 2=Octavos...')

    class Meta:
        verbose_name = 'Fase eliminatoria'
        verbose_name_plural = 'Fases eliminatorias'
        ordering = ['order']

    def __str__(self):
        return self.name


class KnockoutMatch(models.Model):
    """
    Partido de fase eliminatoria.
    Referencia un Match existente y agrega lógica de penales y slots.
    """
    round = models.ForeignKey(KnockoutRound, on_delete=models.CASCADE, related_name='matches', verbose_name='Fase')
    match = models.OneToOneField(Match, on_delete=models.CASCADE, related_name='knockout_match', verbose_name='Partido')

    # Slots de texto hasta que se asignen los equipos reales
    slot_home = models.CharField(max_length=50, blank=True, verbose_name='Slot local', help_text='Ej: 1° Grupo A')
    slot_away = models.CharField(max_length=50, blank=True, verbose_name='Slot visitante', help_text='Ej: 2° Grupo B')

    # Penales (solo si terminó 90 min en empate)
    went_to_penalties = models.BooleanField(default=False, verbose_name='Fue a penales')
    home_penalties = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Penales local')
    away_penalties = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Penales visitante')

    class Meta:
        verbose_name = 'Partido eliminatorio'
        verbose_name_plural = 'Partidos eliminatorios'

    def __str__(self):
        return f'{self.round} — {self.match}'

    @property
    def penalty_winner(self):
        """Retorna 'home' o 'away' según quien ganó en penales."""
        if not self.went_to_penalties:
            return None
        if self.home_penalties is None or self.away_penalties is None:
            return None
        return 'home' if self.home_penalties > self.away_penalties else 'away'