from django import forms
from .models import Tanque

class TanqueForm(forms.ModelForm):
    
    class Meta:
        
        model = Tanque
        fields = ['tipo_combustivel', 'identificador_tanque', 'capacidade_maxima', 'quantidade_disponivel']
        widgets = {
            'tipo_combustivel': forms.Select(attrs={'class': 'form__select'}),
            'identificador_tanque': forms.TextInput(attrs={'class': 'form__input'}),
            'capacidade_maxima': forms.NumberInput(attrs={'class': 'form__input'}),
            'quantidade_disponivel': forms.NumberInput(attrs={'class': 'form__input'}),
        }
        labels = {
            'tipo_combustivel': 'Tipo de Combustível',
            'identificador_tanque': 'Identificador',
            'capacidade_maxima': 'Capacidade do Tanque',
            'quantidade_disponivel': 'Quantidade Disponível',
        }
    