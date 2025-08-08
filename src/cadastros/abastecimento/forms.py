from django import forms
from decimal import Decimal
from .models import Abastecimento, Tanque, Bomba


class AbastecimentoForm(forms.ModelForm):

    class Meta:
        model = Abastecimento
        fields = ['bomba', 'litros_abastecidos', 'valor']

    
    def clean_valor(self):

        valor = self.cleaned_data.get('valor')

        if isinstance(valor, str):
            
            valor_decimal = 0
            valor_corrigido = valor.replace(',', '.')

            if valor.count(','):
                valor_decimal = Decimal(valor_corrigido)
                return valor_decimal
            else:
                valor_decimal = Decimal(valor_corrigido)
                return valor_decimal
        return valor




class TanqueForm(forms.ModelForm):
    
    class Meta:
        model = Tanque
        fields = ['tipo_combustivel', 'quantidade']


class BombaForm(forms.ModelForm):

    class Meta:
        model = Bomba
        fields = ['nome_bomba', 'tanque']

