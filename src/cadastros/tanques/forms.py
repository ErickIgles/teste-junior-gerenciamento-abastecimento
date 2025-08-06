from django import forms
from .models import Tanque


class TanqueForm(forms.ModelForm):
    
    class Meta:
        model = Tanque
        fields = ['tipo_combustivel', 'capacidade_maxima', 'quantidade_disponivel']

