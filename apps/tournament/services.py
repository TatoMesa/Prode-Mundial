from apps.matches.models import Match
from .models import Group, GroupStanding


def recalculate_group_standings(group: Group) -> None:
    """
    Recalcula la tabla de posiciones de un grupo completo
    a partir de todos los partidos finalizados.
    """
    # Resetear todos los standings del grupo
    GroupStanding.objects.filter(group=group).update(
        played=0, won=0, drawn=0, lost=0,
        goals_for=0, goals_against=0, points=0,
    )

    # Obtener todos los partidos finalizados entre equipos del grupo
    team_ids = group.teams.values_list('id', flat=True)
    matches = Match.objects.filter(
        status=Match.Status.FINISHED,
        home_team_id__in=team_ids,
        away_team_id__in=team_ids,
        home_score__isnull=False,
        away_score__isnull=False,
    )

    for match in matches:
        home_standing, _ = GroupStanding.objects.get_or_create(
            group=group, team=match.home_team
        )
        away_standing, _ = GroupStanding.objects.get_or_create(
            group=group, team=match.away_team
        )

        home_standing.played += 1
        away_standing.played += 1
        home_standing.goals_for += match.home_score
        home_standing.goals_against += match.away_score
        away_standing.goals_for += match.away_score
        away_standing.goals_against += match.home_score

        if match.home_score > match.away_score:
            home_standing.won += 1
            home_standing.points += 3
            away_standing.lost += 1
        elif match.away_score > match.home_score:
            away_standing.won += 1
            away_standing.points += 3
            home_standing.lost += 1
        else:
            home_standing.drawn += 1
            away_standing.drawn += 1
            home_standing.points += 1
            away_standing.points += 1

        home_standing.save()
        away_standing.save()