from django.urls import path
from .views import JoinLeagueView, MyLeaguesView, LeagueRankingView

app_name = 'leagues'

urlpatterns = [
    path('join/', JoinLeagueView.as_view(), name='join'),
    path('', MyLeaguesView.as_view(), name='my_leagues'),
    path('<str:code>/ranking/', LeagueRankingView.as_view(), name='ranking'),
]