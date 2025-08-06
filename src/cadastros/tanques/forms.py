from django import forms
from .models import Tanque
from decimal import Decimal

class TanqueForm(forms.ModelForm):
    
    class Meta:
        model = Tanque
        fields = ['tipo_combustivel', 'capacidade_maxima', 'quantidade_disponivel']

    def clean_capacidade_maxima(self):
        capacidade_maxima_decimal = 0

        capacidade_maxima = self.cleaned_data.get('capacidade_maxima')

        if isinstance(capacidade_maxima, str):
            
            if capacidade_maxima.count(','):
                capacidade_maxima_corrigida = capacidade_maxima.replace(',', '.')

                capacidade_maxima_decimal = Decimal(capacidade_maxima_corrigida)
                return capacidade_maxima_decimal

        return capacidade_maxima
    


    def clean_quantiade_disponivel(self):
        quantidade_disponivel_decimal = 0

        quantidade_disponivel = self.cleaned_data.get('quantidade_disponivel')

        if isinstance(quantidade_disponivel, str):

            if quantidade_disponivel.count(','):
                quantidade_disponivel_corrigida = quantidade_disponivel.replace(',', '.')
                quantidade_disponivel_decimal = Decimal(quantidade_disponivel_corrigida)
                return quantidade_disponivel_decimal
        
        return quantidade_disponivel

