
from django.db import models
from django.contrib.auth.models import User
from apps.matches.models import Match


class Prediction(models.Model):
    user       = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='predictions', verbose_name='Usuario')
    match      = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='predictions', verbose_name='Partido')
    home_goals = models.PositiveSmallIntegerField(verbose_name='Goles local')
    away_goals = models.PositiveSmallIntegerField(verbose_name='Goles visitante')
    points     = models.PositiveSmallIntegerField(default=0, verbose_name='Puntos')
    is_exact   = models.BooleanField(default=False, verbose_name='Resultado exacto')
    is_winner  = models.BooleanField(default=False, verbose_name='Ganador acertado')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pronóstico'
        verbose_name_plural = 'Pronósticos'
        unique_together = ('user', 'match')

    def __str__(self):
        return f'{self.user.username}: {self.match} → {self.home_goals}-{self.away_goals}'