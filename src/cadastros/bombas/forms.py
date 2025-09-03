from django import forms

from cadastros.tanques.models import Tanque

from .models import Bomba


class BombaForm(forms.ModelForm):
    nome_bomba = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input'
            }
        ),
        label='Nome da bomba'
    )

    tanque = forms.ModelChoiceField(
        queryset=Tanque.objects.none(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form-input'
            }
        ),
        label='Tanque'
    )

    class Meta:
        model = Bomba
        fields = ['nome_bomba', 'tanque']

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

        if self.empresa:
            self.fields['tanque'].queryset = Tanque.objects.filter(
                empresa=self.empresa
            )

    def clean_nome_bomba(self):
        nome_bomba = self.cleaned_data.get('nome_bomba')

        if not self.empresa:
            raise forms.ValidationError('Empresa não informada para validação')

        if Bomba.objects.filter(
            nome_bomba=nome_bomba,
            empresa=self.empresa
        ).exists():
            raise forms.ValidationError(
                'Há uma bomba cadastrada com esse nome para esta empresa.'
            )
        return nome_bomba

    def clean_tanque(self):
        tanque = self.cleaned_data.get('tanque')

        if tanque and not tanque.ativo:
            raise forms.ValidationError('Este tanque está desativado.')
        return tanque

    def save(self, commit=True):
        bomba = self.instance
        bomba.empresa = self.empresa

        if commit:
            bomba.save()
        return bomba


class BombaUpdateForm(forms.ModelForm):
    status = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Status da Bomba'
    )

    nome_bomba = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input'
            }
        ),
        label='Nome da bomba'
    )

    tanque = forms.ModelChoiceField(
        required=False,
        queryset=Tanque.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        ),
        label='Tanque'
    )

    class Meta:
        model = Bomba
        fields = ['nome_bomba', 'tanque']

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

        if self.empresa:
            self.fields['tanque'].queryset = (
                Tanque.objects
                .filter(empresa=self.empresa)
                .select_related('tipo_combustivel')
            )

    def clean_nome_bomba(self):

        nome_bomba = self.cleaned_data.get('nome_bomba')

        if not self.empresa:

            raise forms.ValidationError('Empresa não informada para validação')

        nome_bomba_existe = Bomba.objects.filter(
            nome_bomba=nome_bomba,
            empresa=self.empresa
        ).exclude(id=self.instance.pk)

        if nome_bomba_existe.exists():

            raise forms.ValidationError(
                'Há uma bomba cadastrada com esse nome para esta empresa.'
            )

        return nome_bomba

    def clean_tanque(self):
        tanque = self.cleaned_data.get('tanque')
        if tanque and not tanque.ativo:
            raise forms.ValidationError('Esta tanque está desativada.')
        return tanque

    def save(self, commit=True):
        bomba = self.instance
        bomba.empresa = self.empresa
        bomba.ativo = self.cleaned_data.get('status')
        if commit:
            bomba.save()
        return bomba
