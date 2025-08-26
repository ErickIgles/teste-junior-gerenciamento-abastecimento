from django import forms

from .models import RegistroAbastecimento
from ..tanques.models import Tanque, Combustivel
from ..bombas.models import Bomba


class AbastecimentoForm(forms.ModelForm):
    tanque = forms.ModelChoiceField(
        required=True,
        queryset=Tanque.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form__input',
            }
        ),
        label='Tanque'
    )
    bomba = forms.ModelChoiceField(
        required=True,
        queryset=Bomba.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form__input',
            }
        ),
        label='Bomba'
    )
    tipo_combustivel = forms.ModelChoiceField(
        required=True,
        queryset=Combustivel.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form__input',
            }
        ),
        label='Tipo de Combustível'
    )
    litros_abastecido = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form__input',
            }
        ),
        label='Litros abastecidos'
    )

    class Meta:
        model = RegistroAbastecimento
        fields = [
            'tanque',
            'bomba',
            'tipo_combustivel',
            'litros_abastecido'
        ]

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        self.usuario_funcionario = kwargs.pop('usuario_funcionario', None)
        super().__init__(*args, **kwargs)

        if self.empresa:
            self.fields['tanque'].queryset = Tanque.objects.filter(
                empresa=self.empresa,
                ativo=True
            )
            self.fields['bomba'].queryset = Bomba.objects.filter(
                empresa=self.empresa,
                ativo=True
            )
            self.fields['tipo_combustivel'].queryset = Combustivel.objects.filter(
                empresa=self.empresa,
                ativo=True
            )

    def clean_litros_abastecido(self):
        litros_abastecido = self.cleaned_data.get('litros_abastecido')
        tanque = self.cleaned_data.get('tanque')

        if litros_abastecido <= 0:
            raise forms.ValidationError(
                'Por favor, informe um valor maior do que 0.'
            )

        if tanque and litros_abastecido > tanque.quantidade_disponivel:
            raise forms.ValidationError(
                'Valor acima da quantidade disponível no tanque.'
            )

        return litros_abastecido

    def clean_tanque(self):
        tanque = self.cleaned_data.get('tanque')

        if tanque and not tanque.ativo:
            raise forms.ValidationError('Este tanque está desativado.')

        return tanque

    def clean_bomba(self):
        bomba = self.cleaned_data.get('bomba')

        if bomba and not bomba.ativo:
            raise forms.ValidationError('Esta bomba está desativada.')

        return bomba

    def save(self, commit=True):

        if self.usuario_funcionario:
            funcionario = self.usuario_funcionario
        else:
            funcionario = self.empresa.usuario_responsavel

        registro_abastecimento = RegistroAbastecimento(
            funcionario=funcionario,
            tanque=self.cleaned_data.get('tanque'),
            bomba=self.cleaned_data.get('bomba'),
            empresa=self.empresa,
            tipo_combustivel=self.cleaned_data.get('tipo_combustivel'),
            litros_abastecido=self.cleaned_data.get('litros_abastecido')
        )

        if commit:
            registro_abastecimento.save()
        return registro_abastecimento


class AbastecimentoUpdateForm(forms.ModelForm):
    tanque = forms.ModelChoiceField(
        required=True,
        queryset=Tanque.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form__input',
            }
        ),
        label='Tanque'
    )
    bomba = forms.ModelChoiceField(
        required=True,
        queryset=Bomba.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form__input',
            }
        ),
        label='Bomba'
    )
    tipo_combustivel = forms.ModelChoiceField(
        required=True,
        queryset=Combustivel.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form__input',
            }
        ),
        label='Tipo de Combustível'
    )
    litros_abastecido = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form__input',
            }
        ),
        label='Litros abastecidos'
    )

    class Meta:
        model = RegistroAbastecimento
        fields = [
            'tanque',
            'bomba',
            'tipo_combustivel',
            'litros_abastecido'
        ]

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        self.usuario_funcionario = kwargs.pop('usuario_funcionario', None)
        super().__init__(*args, **kwargs)

        if self.empresa:
            self.fields['tanque'].queryset = Tanque.objects.filter(
                empresa=self.empresa,
                ativo=True
            )
            self.fields['bomba'].queryset = Bomba.objects.filter(
                empresa=self.empresa,
                ativo=True
            )
            self.fields['tipo_combustivel'].queryset = Combustivel.objects.filter(
                empresa=self.empresa,
                ativo=True
            )

    def clean_litros_abastecido(self):
        litros_abastecido = self.cleaned_data.get('litros_abastecido')
        tanque = self.cleaned_data.get('tanque')

        if litros_abastecido <= 0:
            raise forms.ValidationError(
                'Por favor, informe um valor maior do que 0.'
            )

        if tanque and litros_abastecido > tanque.quantidade_disponivel:
            raise forms.ValidationError(
                'Valor acima da quantidade disponível no tanque.'
            )

        return litros_abastecido

    def clean_tanque(self):
        tanque = self.cleaned_data.get('tanque')

        if tanque and not tanque.ativo:
            raise forms.ValidationError('Este tanque está desativado.')

        return tanque

    def clean_bomba(self):
        bomba = self.cleaned_data.get('bomba')

        if bomba and not bomba.ativo:
            raise forms.ValidationError('Esta bomba está desativada.')

        return bomba

    def save(self, commit=True):

        if self.usuario_funcionario:
            funcionario = self.usuario_funcionario
        else:
            funcionario = self.empresa.usuario_responsavel

        registro_abastecimento = self.instance

        registro_abastecimento.funcionario = funcionario
        registro_abastecimento.tanque
        registro_abastecimento.bomba=self.cleaned_data.get('bomba')
        registro_abastecimento.empresa=self.empresa
        registro_abastecimento.tipo_combustivel=self.cleaned_data.get('tipo_combustivel')
        registro_abastecimento.litros_abastecido=self.cleaned_data.get('litros_abastecido')

        if commit:
            registro_abastecimento.save()
        return registro_abastecimento
