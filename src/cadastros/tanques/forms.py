from django import forms
from .models import Tanque, Combustivel


class TanqueForm(forms.ModelForm):

    tipo_combustivel = forms.ModelChoiceField(
        required=False,
        queryset=Combustivel.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-select',
            }
        ),
        label='Tipo de Combustível'
    )

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

            'identificador_tanque': forms.TextInput(
                attrs={
                    'class': 'form-input'
                }
            ),
            'capacidade_maxima': forms.NumberInput(
                attrs={
                    'class': 'form-input'
                }
            ),
            'quantidade_disponivel': forms.NumberInput(
                attrs={
                    'class': 'form-input'
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

            self.fields['tipo_combustivel'].queryset = Combustivel.objects.filter(
                empresa=self.empresa
            )

    def clean_identificador_tanque(self):

        identificador_tanque = self.cleaned_data.get('identificador_tanque')

        id_tanque_busca = Tanque.objects.filter(
            identificador_tanque=identificador_tanque,
            empresa=self.empresa
        )

        if id_tanque_busca.exists():

            raise forms.ValidationError('Identificador já cadastrado.')

        return identificador_tanque

    def clean_capacidade_maxima(self):

        capacidade_maxima = self.cleaned_data.get(
            'capacidade_maxima'
        )

        if capacidade_maxima is None:

            raise forms.ValidationError(
                """
                Informe um valor.
                """)

        if capacidade_maxima < 0:

            raise forms.ValidationError(
                """
                A capacidade do tanque não pode ser negativa
                """)

        return capacidade_maxima

    def clean_quantidade_disponivel(self):

        quantidade_disponivel = self.cleaned_data.get(
            'quantidade_disponivel'
        )

        if quantidade_disponivel is None:
            raise forms.ValidationError(
                """
                Informe um valor. 
                """
            )

        if quantidade_disponivel < 0:

            raise forms.ValidationError(
                """
                A quantidade disponível no tanque
                não pode ser negativa.
                """)

        return quantidade_disponivel

    def clean(self):
        cleaned_data = super().clean()

        quantidade = self.cleaned_data.get(
            'quantidade_disponivel'
        )
        capacidade = self.cleaned_data.get(
            'capacidade_maxima'
        )

        if quantidade is not None and capacidade is not None:
            if quantidade > capacidade:
                self.add_error(
                    "quantidade_disponivel",
                    """
                    A quantidade não pode exceder
                    a capacidade máxima.
                    """
                )
        return cleaned_data

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
        ]
        widgets = {
            'tipo_combustivel': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
            'identificador_tanque': forms.TextInput(
                attrs={
                    'class': 'form-input'
                }
            ),
            'capacidade_maxima': forms.NumberInput(
                attrs={
                    'class': 'form-input'
                }
            ),
        }
        labels = {
            'tipo_combustivel': 'Tipo de Combustível',
            'identificador_tanque': 'Identificador',
            'capacidade_maxima': 'Capacidade do Tanque',
        }

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

        if self.empresa:
            self.fields['tipo_combustivel'].queryset = Combustivel.objects.filter(
                empresa=self.empresa
            )

    def clean_identificador_tanque(self):
        identificador_tanque = self.cleaned_data.get('identificador_tanque')

        if not self.empresa:
            raise forms.ValidationError('Empresa não informada para validação')

        tanque = Tanque.objects.filter(
            identificador_tanque=identificador_tanque,
            empresa=self.empresa
        ).exclude(
            id=self.instance.pk
        )

        if tanque.exists():
            raise forms.ValidationError('Identificador já cadastrado.')
        return identificador_tanque

    def clean_capacidade_maxima(self):
        capacidade_maxima = self.cleaned_data.get(
            'capacidade_maxima'
        )

        if capacidade_maxima is None:

            raise forms.ValidationError(
                """
                Informe um valor.
                """
            )

        if capacidade_maxima < 0:

            raise forms.ValidationError(
                """A capacidade máxima não pode ser
                negativo."""
            )

        return capacidade_maxima

    def save(self, commit=True):

        tanque = super().save(commit=False)
        tanque.empresa = self.empresa
        tanque.ativo = self.cleaned_data.get('status')

        if commit:

            tanque.save()

        return tanque


class CombustivelForm(forms.ModelForm):

    nome_combustivel = forms.CharField(
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-select'
            }
        ),
        label='Tipo de combustível'
    )

    valor_base = forms.DecimalField(
        localize=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input'
            }
        ),
        label='Valor base: R$'
    )

    imposto = forms.DecimalField(
        localize=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input'
            }
        ),
        label='Percentual do imposto: %'
    )

    valor_compra = forms.DecimalField(
        localize=True,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input'
            }
        ),
        label='Valor de compra: R$'
    )

    class Meta:
        model = Combustivel
        fields = [
            'nome_combustivel',
            'valor_base',
            'imposto',
            'valor_compra'
        ]

    def __init__(self, *args, **kwargs):

        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

    def clean_nome_combustivel(self):

        nome_combustivel = self.cleaned_data.get(
            'nome_combustivel'
        )

        if len(nome_combustivel) < 3:

            raise forms.ValidationError(
                """
                O nome do combustivel
                tem que ter mais do que 3 caracteres.
                """
            )

        return nome_combustivel

    def clean_valor_base(self):

        valor_base = self.cleaned_data.get(
            'valor_base'
        )

        if valor_base < 0:

            raise forms.ValidationError(
                """
                O valor base não pode ser negativo.
                """
            )

        return valor_base

    def clean_imposto(self):

        imposto = self.cleaned_data.get(
            'imposto'
        )

        if imposto < 0:
            raise forms.ValidationError(
                """ O valor do imposto não pode ser negativo."""
            )

        return imposto

    def save(self, commit=True):

        combustivel = super().save(commit=False)

        combustivel.empresa = self.empresa

        if commit:

            combustivel.save()

        return combustivel
