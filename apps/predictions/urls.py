from django.urls import path
from .views import (
    PredictionCreateUpdateView,
    UserPredictionsListView,
    RankingView,
    PredictionEditView,
)

app_name = 'predictions'

urlpatterns = [
    path('', UserPredictionsListView.as_view(), name='my_predictions'),
    #path('ranking/', RankingView.as_view(), name='ranking'),
    path('match/<int:match_pk>/create/', PredictionCreateUpdateView.as_view(), name='create'),
    path('<int:pk>/edit/', PredictionEditView.as_view(), name='edit'),
]