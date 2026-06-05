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
        default='Premios Primera Ronda',
        verbose_name='Premios Primera Ronda',
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

    prizes_title2 = models.CharField(
        max_length=100, blank=True,
        default='Premios Resultados Partido de Argentina',
        verbose_name='Premios Resultados Partido de Argentina',
    )

    prize_4_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 4 — nombre')
    prize_4_description = models.TextField(blank=True, verbose_name='Premio 4 — descripción')
    prize_4_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 4 — imagen')

    prize_5_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 5 — nombre')
    prize_5_description = models.TextField(blank=True, verbose_name='Premio 5 — descripción')
    prize_5_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 5 — imagen')

    prize_6_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 6 — nombre')
    prize_6_description = models.TextField(blank=True, verbose_name='Premio 6 — descripción')
    prize_6_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 6 — imagen')
    
    prizes_title3 = models.CharField(
        max_length=100, blank=True,
        default='Premios Resultados Partido de Argentina exacto',
        verbose_name='Premios Resultados Partido de Argentina exacto',
    )
    prize_7_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 7 — nombre')
    prize_7_description = models.TextField(blank=True, verbose_name='Premio 7 — descripción')
    prize_7_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 7 — imagen')

    prize_8_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 8 — nombre')
    prize_8_description = models.TextField(blank=True, verbose_name='Premio 8 — descripción')
    prize_8_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 8 — imagen')

    prize_9_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 9 — nombre')
    prize_9_description = models.TextField(blank=True, verbose_name='Premio 9 — descripción')
    prize_9_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 9 — imagen')
   
    prizes_title4 = models.CharField(
        max_length=100, blank=True,
        default='Premios Mundial Completo',
        verbose_name='Premios Mundial Completo',
    )
  
    prize_10_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 10 — nombre')
    prize_10_description = models.TextField(blank=True, verbose_name='Premio 10 — descripción')
    prize_10_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 10 — imagen')

    prize_11_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 11 — nombre')
    prize_11_description = models.TextField(blank=True, verbose_name='Premio 11 — descripción')
    prize_11_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 11 — imagen')

    prize_12_name = models.CharField(max_length=100, blank=True, verbose_name='Premio 12 — nombre')
    prize_12_description = models.TextField(blank=True, verbose_name='Premio 12 — descripción')
    prize_12_image = models.ImageField(upload_to='leagues/prizes/', null=True, blank=True, verbose_name='Premio 12 — imagen')

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
        """Retorna un listado plano de todos los premios cargados (del 1 al 12)."""
        result = []
        medals = ['🥇', '🥈', '🥉']
        
        for i in range(1, 13):
            name = getattr(self, f'prize_{i}_name', '').strip()
            if name:
                # Calculamos la posición dentro de su tanda de 3 para asignarle medalla
                # Los premios 1, 4, 7, 10 son 1er puesto (🥇)
                # Los premios 2, 5, 8, 11 son 2do puesto (🥈)
                # Los premios 3, 6, 9, 12 son 3er puesto (🥉)
                idx = (i - 1) % 3 
                
                result.append({
                    'position': i,
                    'medal': medals[idx],
                    'name': name,
                    'description': getattr(self, f'prize_{i}_description', ''),
                    'image': getattr(self, f'prize_{i}_image', None),
                })
        return result
    @property
    def prize_sections(self):
        """Retorna las secciones organizadas de premios, ignorando las vacías."""
        medals = ['🥇', '🥈', '🥉']
        
        # Mapeamos los bloques y les asignamos el texto por defecto directamente en el código
        sections_config = [
            {'title': self.prizes_title or 'Premios Primera Ronda', 'range': range(1, 4)},
            {'title': self.prizes_title2 or 'Premios Resultados Partido de Argentina', 'range': range(4, 7)},
            {'title': self.prizes_title3 or 'Premios Resultados Partido de Argentina exacto', 'range': range(7, 10)},
            {'title': self.prizes_title4 or 'Premios Mundial Completo', 'range': range(10, 13)},
        ]
        
        structured_sections = []
        
        for config in sections_config:
            section_prizes = []
            for idx, num in enumerate(config['range']):
                name = getattr(self, f'prize_{num}_name', '').strip()
                if name:
                    section_prizes.append({
                        'name': name,
                        'description': getattr(self, f'prize_{num}_description', ''),
                        'image': getattr(self, f'prize_{num}_image', None),
                        'medal': medals[idx] if idx < len(medals) else '🏆'
                    })
            
            # Solo sumamos la sección si tiene premios reales
            if section_prizes:
                structured_sections.append({
                    'title': config['title'],
                    'prizes': section_prizes
                })
                
        return structured_sections
    
    @property
    def has_prizes(self):
        """Devuelve True si al menos un premio tiene nombre."""
        return any(bool(getattr(self, f'prize_{i}_name', '').strip()) for i in range(1, 13))

    @property
    def has_prizes(self):
        return bool(self.prize_1_name or self.prize_2_name or self.prize_3_name or self.prize_4_name or self.prize_5_name or self.prize_6_name or self.prize_7_name or self.prize_8_name or self.prize_9_name or self.prize_10_name or self.prize_11_name or self.prize_12_name)

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