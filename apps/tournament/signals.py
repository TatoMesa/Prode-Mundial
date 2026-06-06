from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.matches.models import Match


@receiver(post_save, sender=Match)
def recalculate_standings_on_finish(sender, instance, **kwargs):
    """Recalcula la tabla del grupo cuando un partido se marca como Finalizado."""
    if instance.status != Match.Status.FINISHED:
        return
    if instance.home_score is None or instance.away_score is None:
        return

    from apps.tournament.models import Group
    from apps.tournament.services import recalculate_group_standings

    # Buscar si el partido pertenece a algún grupo
    groups = Group.objects.filter(
        teams=instance.home_team
    ).filter(
        teams=instance.away_team
    )
    for group in groups:
        recalculate_group_standings(group)