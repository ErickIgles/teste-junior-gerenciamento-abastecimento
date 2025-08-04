from django import forms

from .models import Abastecimento, Tanque, Bomba


class AbastecimentoForm(forms.ModelForm):

    class Meta:
        model = Abastecimento
        fields = ['bomba', 'litros_abastecidos', 'valor']


class TanqueForm(forms.ModelForm):
    
    class Meta:
        model = Tanque
        fields = ['tipo_combustivel', 'quantidade']


class BombaForm(forms.ModelForm):

    class Meta:
        model = Bomba
        fields = ['nome_bomba', 'tanque']

