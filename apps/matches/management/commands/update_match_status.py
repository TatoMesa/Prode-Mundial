from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.matches.models import Match


class Command(BaseCommand):
    help = 'Actualiza el estado de los partidos según la hora actual'

    def handle(self, *args, **options):
        now = timezone.now()

        # Pendiente → En juego cuando llega la hora del kickoff
        started = Match.objects.filter(
            status=Match.Status.PENDING,
            kickoff_time__lte=now,
        ).update(status=Match.Status.IN_PROGRESS)

        self.stdout.write(f'{started} partido(s) → En juego')