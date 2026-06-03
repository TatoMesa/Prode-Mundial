import random
import string
from django.db import models
from django.contrib.auth.models import User


def generate_code():
    """Genera un código único de 6 caracteres alfanuméricos en mayúsculas."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


class League(models.Model):
    """Torneo privado al que los usuarios se unen con un código."""
    name = models.CharField(max_length=100, verbose_name='Nombre')
    code = models.CharField(
        max_length=6,
        unique=True,
        default=generate_code,
        verbose_name='Código de acceso',
    )
    members = models.ManyToManyField(
        User,
        through='LeagueMembership',
        related_name='leagues',
        blank=True,
    )
    is_active = models.BooleanField(default=True, verbose_name='Activa')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Liga privada'
        verbose_name_plural = 'Ligas privadas'

    def __str__(self):
        return f'{self.name} ({self.code})'


class LeagueMembership(models.Model):
    """Relación entre usuario y liga privada."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='memberships')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Miembro'
        verbose_name_plural = 'Miembros'
        unique_together = ('user', 'league')

    def __str__(self):
        return f'{self.user.username} → {self.league.name}'