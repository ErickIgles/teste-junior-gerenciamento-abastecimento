from django import forms
from .models import Tanque, Combustivel





class TanqueForm(forms.ModelForm):
    tipo_combustivel = forms.ModelChoiceField(
        required=False,
        queryset=Combustivel.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form__input',
            }
        ),
        label='Tipo de Combustível'
    )

    class Meta:
        
        model = Tanque
        fields = [
            'tipo_combustivel', 
            'identificador_tanque', 
            'capacidade_maxima', 
            'quantidade_disponivel'
            ]
        widgets = {
            'tipo_combustivel': forms.Select(
                attrs={
                    'class': 'form__select'
                }
            ),
            'identificador_tanque': forms.TextInput(
                attrs={
                    'class': 'form__input'
                }
            ),
            'capacidade_maxima': forms.NumberInput(
                attrs={
                    'class': 'form__input'
                }
            ),
            'quantidade_disponivel': forms.NumberInput(
                attrs={
                    'class': 'form__input'
                }    
            ),
        }
        labels = {
            'tipo_combustivel': 'Tipo de Combustível',
            'identificador_tanque': 'Identificador',
            'capacidade_maxima': 'Capacidade do Tanque',
            'quantidade_disponivel': 'Quantidade Disponível',
        }


    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

        if self.empresa:
            self.fields['tipo_combustivel'].queryset = Combustivel.objects.filter(empresa=self.empresa)

    def clean_identificador_tanque(self):
        identificador_tanque = self.cleaned_data.get('identificador_tanque')

        if Tanque.objects.filter(
            identificador_tanque=identificador_tanque
            ).exists():
            raise forms.ValidationError('Identificador já cadastrado.')
        return identificador_tanque
    

    def save(self, commit=True):
    
        tanque = self.instance
        tanque.empresa = self.empresa

        if commit:
            tanque.save()

        return tanque


class TanqueUpdateForm(forms.ModelForm):
    status = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox'
            }
        ), 
        label='Status do Tanque'
    )
    class Meta:
        
        model = Tanque
        fields = [
            'tipo_combustivel', 
            'identificador_tanque', 
            'capacidade_maxima', 
            'quantidade_disponivel'
        ]
        widgets = {
            'tipo_combustivel': forms.Select(
                attrs={
                    'class': 'form__select'
                }
            ),
            'identificador_tanque': forms.TextInput(
                attrs={
                    'class': 'form__input'
                }
            ),
            'capacidade_maxima': forms.NumberInput(
                attrs={
                    'class': 'form__input'
                }
            ),
            'quantidade_disponivel': forms.NumberInput(
                attrs={
                    'class': 'form__input'
                }
            ),
        }
        labels = {
            'tipo_combustivel': 'Tipo de Combustível',
            'identificador_tanque': 'Identificador',
            'capacidade_maxima': 'Capacidade do Tanque',
            'quantidade_disponivel': 'Quantidade Disponível',
        }


    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

        if self.empresa:
            self.fields['tipo_combustivel'].queryset = Combustivel.objects.filter(empresa=self.empresa)


    def clean_identificador_tanque(self):
        identificador_tanque = self.cleaned_data.get('identificador_tanque')
        
        if not self.empresa:
            raise forms.ValidationError('Empresa não informada para validação')

        if Tanque.objects.filter(
            identificador_tanque=identificador_tanque, 
            empresa=self.empresa
            ).exclude(id=self.instance.pk).exists():
            raise forms.ValidationError('Identificador já cadastrado.')
        return identificador_tanque
    
    def clean_quantidade_disponivel(self):
        quantidade_disponivel = self.cleaned_data.get('quantidade_disponivel')
        capacidade_maxima = self.cleaned_data.get('capacidade_maxima')


        if quantidade_disponivel < 0:
            raise forms.ValidationError(
            'A quantidade não pode ser negativo.'
                )
        if quantidade_disponivel > capacidade_maxima:
            raise forms.ValidationError(
            'A quantidade de combustível não pode ser maior que a capacidade máxima do tanque.'
            )
        return quantidade_disponivel

    def save(self, commit=True):
        
        tanque = super().save(commit=False)
        tanque.empresa = self.empresa
        tanque.ativo = self.cleaned_data.get('status')

        if commit:
            tanque.save()

        return tanque