# apps/matches/api_views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Match
from .serializers import MatchSerializer


class MatchAPIView(APIView):
    """Endpoint que devuelve el estado actual de un partido en JSON."""

    def get(self, request, pk):
        try:
            match = Match.objects.select_related('home_team', 'away_team').get(pk=pk)
        except Match.DoesNotExist:
            return Response({'error': 'Partido no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MatchSerializer(match)
        return Response(serializer.data)