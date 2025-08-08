from django import forms
from .models import RegistroAbastecimento


class AbastecimentoForm(forms.ModelForm):

    class Meta:
        model = RegistroAbastecimento
        fields = ['tanque', 'tipo_combustivel', 'litros_abastecer']

        widgets = {
            'tanque': forms.Select(attrs={'class':'form__select'}),
            'tipo_combustivel': forms.Select(attrs={'class': 'form__select'}),
            'litros_abastecer': forms.NumberInput(attrs={'class': 'form__input'}),
        }
        labels = {
            'tanque': 'Tanque',
            'tipo_combustivel': 'Tipo de Combustível',
            'litros_abastecer': 'Litros a Abastecer',
        }

