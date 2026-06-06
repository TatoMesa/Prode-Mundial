from django.urls import path
from .views import GroupStandingsView, KnockoutView

app_name = 'tournament'

urlpatterns = [
    path('groups/', GroupStandingsView.as_view(), name='groups'),
    path('knockout/', KnockoutView.as_view(), name='knockout'),
]