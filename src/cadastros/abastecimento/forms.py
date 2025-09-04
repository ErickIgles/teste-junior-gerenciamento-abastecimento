from django import forms

from .models import RegistroAbastecimento
from ..tanques.models import Tanque, Combustivel
from ..bombas.models import Bomba


class AbastecimentoForm(forms.ModelForm):
    tanque = forms.ModelChoiceField(
        required=False,
        queryset=Tanque.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'readonly': 'readonly',
                'disabled': 'disabled'
            }
        ),
        label='Tanque'
    )
    bomba = forms.ModelChoiceField(
        required=True,
        queryset=Bomba.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
            }
        ),
        label='Bomba'
    )
    tipo_combustivel = forms.ModelChoiceField(
        required=True,
        queryset=Combustivel.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
            }
        ),
        label='Tipo de Combustível'
    )
    litros_abastecido = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-input',
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
            self.fields['bomba'].queryset = Bomba.objects.filter(
                empresa=self.empresa,
                ativo=True
            )
            self.fields['tipo_combustivel'].queryset = Combustivel.objects.filter(
                empresa=self.empresa,
                ativo=True
            )

        if 'bomba' in self.data:

            try:

                bomba_id = int(self.data.get('bomba'))
                bomba = Bomba.objects.get(
                    id=bomba_id,
                    empresa=self.empresa
                )
                self.fields['tanque'].initial = bomba.tanque
            except (ValueError, Bomba.DoesNotExist):
                pass

        elif self.instance.pk and self.instance.bomba:
            self.fields['tanque'].initial = self.instance.bomba.tanque

    def clean_litros_abastecido(self):
        litros_abastecido = self.cleaned_data.get('litros_abastecido')
        bomba = self.cleaned_data.get('bomba')

        if litros_abastecido <= 0:
            raise forms.ValidationError(
                'Por favor, informe um valor maior do que 0.'
            )

        if bomba and litros_abastecido > bomba.tanque.quantidade_disponivel:
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

        if bomba and not bomba.tanque:
            raise forms.ValidationError(
                """Esta bomba não está vinculada a nenhum tanque."""
            )

        return bomba

    def clean(self):
        cleaned_data = super().clean()

        bomba = cleaned_data.get('bomba')

        if bomba and bomba.tanque:

            tipo_combustivel = cleaned_data.get('tipo_combustivel')

            if tipo_combustivel != bomba.tanque.tipo_combustivel:
                self.add_error(
                    'tipo_combustivel',
                    'O tipo de combustível é diferente do que está no tanque.'
                )
        return cleaned_data

    def save(self, commit=True):

        if self.usuario_funcionario:
            funcionario = self.usuario_funcionario
        else:
            funcionario = self.empresa.usuario_responsavel

        bomba = self.cleaned_data.get('bomba')

        if not bomba:
            raise forms.ValidationError(
                'Selecioe uma bomba'
            )

        if not bomba.tanque:
            raise forms.ValidationError(
                'A bomba selecionada não possui um tanque associado.'
            )

        registro_abastecimento = RegistroAbastecimento(
            funcionario=funcionario,
            tanque=bomba.tanque,
            bomba=bomba,
            empresa=self.empresa,
            tipo_combustivel=bomba.tanque.tipo_combustivel,
            litros_abastecido=self.cleaned_data.get('litros_abastecido')
        )

        if commit:
            registro_abastecimento.save()
        return registro_abastecimento


class AbastecimentoUpdateForm(forms.ModelForm):
    tanque = forms.ModelChoiceField(
        required=False,
        queryset=Tanque.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'readonly': 'readonly',
                'disabled': 'disabled'
            }
        ),
        label='Tanque'
    )
    bomba = forms.ModelChoiceField(
        required=True,
        queryset=Bomba.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
            }
        ),
        label='Bomba'
    )
    tipo_combustivel = forms.ModelChoiceField(
        required=True,
        queryset=Combustivel.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
            }
        ),
        label='Tipo de Combustível'
    )
    litros_abastecido = forms.DecimalField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-input',
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

        if bomba and not bomba.tanque:
            raise forms.ValidationError(
                """Esta bomba não está vinculada a nenhum tanque."""
            )

        return bomba

    def clean(self):
        cleaned_data = super().clean()

        bomba = cleaned_data.get('bomba')

        if bomba and bomba.tanque:

            tipo_combustivel = cleaned_data.get('tipo_combustivel')

            if tipo_combustivel != bomba.tanque.tipo_combustivel:
                self.add_error(
                    'tipo_combustivel',
                    'O tipo de combustível é diferente do que está no tanque.'
                )
        return cleaned_data

    def save(self, commit=True):

        if self.usuario_funcionario:
            funcionario = self.usuario_funcionario
        else:
            funcionario = self.empresa.usuario_responsavel

        registro_abastecimento = self.instance

        bomba = self.cleaned_data.get('bomba')

        if not bomba:
            raise forms.ValidationError("Selecione uma bomba.")

        if not bomba.tanque:
            raise forms.ValidationError("A bomba selecionada não possui um tanque associado.")

        registro_abastecimento.funcionario = funcionario
        registro_abastecimento.bomba=bomba
        registro_abastecimento.tanque = bomba.tanque
        registro_abastecimento.empresa=self.empresa
        registro_abastecimento.tipo_combustivel=self.cleaned_data.get('tipo_combustivel')
        registro_abastecimento.litros_abastecido=self.cleaned_data.get('litros_abastecido')

        if commit:
            registro_abastecimento.save()
        return registro_abastecimento
