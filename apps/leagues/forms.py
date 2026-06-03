from django import forms
from .models import League


class JoinLeagueForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        widget=forms.TextInput(attrs={
            'class': 'form-control form-control-lg text-center text-uppercase',
            'placeholder': 'XXXXXX',
            'autocomplete': 'off',
            'style': 'letter-spacing: 6px; font-weight: bold;',
        }),
        label='Código de liga',
    )

    def clean_code(self):
        code = self.cleaned_data['code'].upper().strip()
        try:
            league = League.objects.get(code=code, is_active=True)
        except League.DoesNotExist:
            raise forms.ValidationError('Código incorrecto o liga inactiva.')
        return code