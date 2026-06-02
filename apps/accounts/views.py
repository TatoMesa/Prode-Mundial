from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.contrib import messages

from .forms import RegisterForm, ProfileUpdateForm
from .models import UserProfile


class RegisterView(CreateView):
    """Registro de nuevos usuarios. Redirige al login tras registro exitoso."""
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, '¡Cuenta creada exitosamente! Iniciá sesión para continuar.')
        return response


class CustomLoginView(LoginView):
    """Login con template personalizado."""
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


from django.db.models import Sum, Count, Q

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['first_name'].initial = self.request.user.first_name
        form.fields['last_name'].initial = self.request.user.last_name
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.predictions.models import Prediction
        stats = Prediction.objects.filter(user=self.request.user).aggregate(
            total=Count('id'),
            total_points=Sum('points'),
            exact_count=Count('id', filter=Q(is_exact=True)),
        )
        context['profile_stats'] = {
            'total': stats['total'] or 0,
            'total_points': stats['total_points'] or 0,
            'exact_count': stats['exact_count'] or 0,
        }
        return context

    def form_valid(self, form):
        user = self.request.user
        user.first_name = form.cleaned_data.get('first_name', '')
        user.last_name = form.cleaned_data.get('last_name', '')
        user.save()
        messages.success(self.request, 'Perfil actualizado correctamente.')
        return super().form_valid(form)