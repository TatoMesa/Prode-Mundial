from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import RegisterView, CustomLoginView, ProfileUpdateView
from django.views.generic import TemplateView
 
app_name = 'accounts'
 
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('terminos-y-condiciones/', TemplateView.as_view(template_name='accounts/terminos_condiciones.html'), name='terminos_condiciones'),
]
 