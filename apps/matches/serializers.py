# apps/matches/serializers.py
from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    home_team_name = serializers.CharField(source='home_team.name')
    home_team_code = serializers.CharField(source='home_team.code')
    home_team_flag = serializers.CharField(source='home_team.flag')
    away_team_name = serializers.CharField(source='away_team.name')
    away_team_code = serializers.CharField(source='away_team.code')
    away_team_flag = serializers.CharField(source='away_team.flag')
    status_display = serializers.CharField(source='get_status_display')
    is_locked = serializers.BooleanField()

    class Meta:
        model = Match
        fields = [
            'id', 'status', 'status_display', 'is_locked',
            'home_team_name', 'home_team_code', 'home_team_flag',
            'away_team_name', 'away_team_code', 'away_team_flag',
            'home_score', 'away_score',
            'kickoff_time',
        ]