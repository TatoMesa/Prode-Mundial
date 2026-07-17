from django.urls import path
from .views import MatchListView, MatchDetailView
from .api_views import MatchAPIView

app_name = 'matches'

urlpatterns = [
    path('', MatchListView.as_view(), name='list'),
    path('<int:pk>/', MatchDetailView.as_view(), name='detail'),
    path('api/<int:pk>/', MatchAPIView.as_view(), name='api_match'),
]