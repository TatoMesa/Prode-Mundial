
def _get_winner(home: int, away: int) -> str:
    if home > away:
        return 'home'
    if away > home:
        return 'away'
    return 'draw'


def calculate_points(real_home, real_away, pred_home, pred_away):
    """Retorna (points, is_exact, is_winner)."""
    is_exact = (real_home == pred_home and real_away == pred_away)
    is_winner = (_get_winner(real_home, real_away) == _get_winner(pred_home, pred_away))

    if is_exact:
        return 5, True, True
    if is_winner:
        return 2, False, True
    return 0, False, False


def recalculate_for_match(match) -> None:
    """Recalcula y guarda los puntos de todos los pronósticos de un partido finalizado."""
    from apps.predictions.models import Prediction

    if match.home_score is None or match.away_score is None:
        return

    predictions = list(Prediction.objects.filter(match=match))
    for p in predictions:
        p.points, p.is_exact, p.is_winner = calculate_points(
            match.home_score, match.away_score,
            p.home_goals, p.away_goals,
        )
    Prediction.objects.bulk_update(predictions, ['points', 'is_exact', 'is_winner'])