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
    logo = models.ImageField(
        upload_to='leagues/logos/',
        null=True,
        blank=True,
        verbose_name='Logo de la liga',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    # ── Sección de premios ─────────────────────────────────────────────────
    prizes_title = models.CharField(
        max_length=100, blank=True,
        default='Premios',
        verbose_name='Título sección premios',
    )
    prize_1_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 1 — nombre')
    prize_1_description = models.TextField(blank=True, verbose_name='Premio 1 — descripción')
    prize_1_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 1 — imagen')

    prize_2_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 2 — nombre')
    prize_2_description = models.TextField(blank=True, verbose_name='Premio 2 — descripción')
    prize_2_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 2 — imagen')

    prize_3_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 3 — nombre')
    prize_3_description = models.TextField(blank=True, verbose_name='Premio 3 — descripción')
    prize_3_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 3 — imagen')

    prize_4_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 4 — nombre')
    prize_4_description = models.TextField(blank=True, verbose_name='Premio 4 — descripción')
    prize_4_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 4 — imagen')
    # ── Sección de marketing ───────────────────────────────────────────────
    marketing_title = models.CharField(
        max_length=100, blank=True,
        verbose_name='Marketing — título',
    )
    marketing_text = models.TextField(blank=True, verbose_name='Marketing — texto')
    marketing_image = models.ImageField(
        upload_to='leagues/marketing/', null=True, blank=True,
        verbose_name='Marketing — imagen',
    )
    marketing_link_text = models.CharField(
        max_length=100, blank=True,
        verbose_name='Marketing — texto del botón',
    )
    marketing_link_url = models.URLField(
        blank=True,
        verbose_name='Marketing — URL del botón',
    )

    class Meta:
        verbose_name = 'Liga privada'
        verbose_name_plural = 'Ligas privadas'

    def __str__(self):
        return f'{self.name} ({self.code})'

    @property
    def prizes(self):
        """Retorna solo los premios que tienen nombre cargado."""
        result = []
        for i in (1, 2, 3, 4):
            name = getattr(self, f'prize_{i}_name')
            if name:
                result.append({
                    'position': i,
                    'medal': ['🥇', '🥈', '🥉', '🏅'][i - 1],
                    'name': name,
                    'description': getattr(self, f'prize_{i}_description'),
                    'image': getattr(self, f'prize_{i}_image'),
                })
        return result

    @property
    def has_prizes(self):
        return bool(self.prize_1_name or self.prize_2_name or self.prize_3_name)

    @property
    def has_marketing(self):
        return bool(self.marketing_title or self.marketing_text)
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