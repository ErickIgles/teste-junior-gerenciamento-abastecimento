from django import forms
from .models import RegistroAbastecimento

from ..tanques.models import Tanque

class AbastecimentoForm(forms.ModelForm):

    class Meta:
        model = RegistroAbastecimento
        fields = ['tanque', 'tipo_combustivel', 'litros_abastecido']

        widgets = {
            'tanque': forms.Select(attrs={'class':'form__select'}),
            'tipo_combustivel': forms.Select(attrs={'class': 'form__select'}),
            'litros_abastecido': forms.NumberInput(attrs={'class': 'form__input'}),
        }
        labels = {
            'tanque': 'Tanque',
            'tipo_combustivel': 'Tipo de Combustível',
            'litros_abastecido': 'Litros Abastecido',
        }


    def clean_litros_abastecido(self):

        litros_abastecido = self.cleaned_data.get('litros_abastecido')
        tanque = self.cleaned_data.get('tanque')


        if litros_abastecido < 0:
            raise forms.ValidationError('Por favor, informe um valor positivo.')
        if litros_abastecido == 0:
            raise forms.ValidationError('Por favor, informe um valor maior do que 0.')
        if litros_abastecido > tanque.quantidade_disponivel:
            raise forms.ValidationError('Valor acima da quantidade disponível no tanque.') 
        return litros_abastecido

        