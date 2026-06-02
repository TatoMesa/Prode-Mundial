from django.db import models
from django.utils import timezone


class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nombre')
    code = models.CharField(max_length=3, unique=True, verbose_name='Código')
    flag = models.CharField(max_length=10, blank=True, verbose_name='Emoji bandera')

    class Meta:
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
        ordering = ['name']

    def __str__(self):
        return f'{self.flag} {self.name}'.strip()


class Match(models.Model):
    class Status(models.TextChoices):
        PENDING     = 'PENDING',     'Pendiente'
        IN_PROGRESS = 'IN_PROGRESS', 'En juego'
        FINISHED    = 'FINISHED',    'Finalizado'

    home_team    = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='home_matches', verbose_name='Local')
    away_team    = models.ForeignKey(Team, on_delete=models.PROTECT, related_name='away_matches', verbose_name='Visitante')
    kickoff_time = models.DateTimeField(verbose_name='Fecha y hora')
    home_score   = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Goles local')
    away_score   = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Goles visitante')
    status       = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING, verbose_name='Estado')

    class Meta:
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        ordering = ['kickoff_time']

    def __str__(self):
        return f'{self.home_team} vs {self.away_team} — {self.kickoff_time:%d/%m/%Y %H:%M}'

    @property
    def is_locked(self):
        from django.conf import settings
        lock_minutes = getattr(settings, 'PREDICTION_LOCK_MINUTES', 10)
        delta = self.kickoff_time - timezone.now()
        return delta.total_seconds() < lock_minutes * 60

    @property
    def result_winner(self):
        if self.home_score is None or self.away_score is None:
            return None
        if self.home_score > self.away_score:
            return 'home'
        if self.away_score > self.home_score:
            return 'away'
        return 'draw'