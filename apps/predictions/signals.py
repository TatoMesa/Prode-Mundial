# apps/predictions/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.matches.models import Match


@receiver(post_save, sender=Match)
def recalculate_on_match_finish(sender, instance, **kwargs):
    """Recalcula puntajes automáticamente cuando un partido se marca como Finalizado."""
    if instance.status == Match.Status.FINISHED:
        from apps.predictions.scoring import recalculate_for_match
        recalculate_for_match(instance)