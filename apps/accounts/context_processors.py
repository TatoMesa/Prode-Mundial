from django.db.models import Sum


def user_points(request):
    """Inyecta los puntos totales del usuario en todos los templates."""
    if request.user.is_authenticated:
        from apps.predictions.models import Prediction
        total = Prediction.objects.filter(
            user=request.user
        ).aggregate(total=Sum('points'))['total'] or 0
        return {'user_total_points': total}
    return {'user_total_points': 0}