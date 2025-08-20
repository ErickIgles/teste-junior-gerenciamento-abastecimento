from django import forms
from .models import Bomba
from cadastros.tanques.models import Tanque




class BombaForm(forms.ModelForm):
    nome_bomba = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form__input'
            }
        ),
        label='Nome da bomba'
    )

    tanque = forms.ModelChoiceField(
        queryset=Tanque.objects.none(),
        required=False,
        widget=forms.Select(
            attrs={
                'class': 'form__input'
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
            self.fields['tanque'].queryset = Tanque.objects.filter(empresa=self.empresa)

    
    def clean_nome_bomba(self):
        nome_bomba = self.cleaned_data.get('nome_bomba')

        if not self.empresa:
            raise forms.ValidationError('Empresa não informada para validação')
        
        if Bomba.objects.filter(
            nome_bomba=nome_bomba, 
            empresa=self.empresa).exists():
            raise forms.ValidationError('Há uma bomba cadastrada com esse nome para esta empresa.')
        return nome_bomba
    
    def clean_tanque(self):
        tanque = self.cleaned_data.get('tanque')

        if tanque and not tanque.ativo:
            raise forms.ValidationError('Este tanque está desativado.')
        return tanque
    
    def save(self, commit=True):
        usuario = self.request.user
        bomba = self.instance
        bomba.empresa = usuario

        if commit:
            bomba.save()
        return bomba


class BombaUpdateForm(forms.ModelForm):
    status = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'checkbox'}), label='Status do tanque')

    nome_bomba = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form__input'
            }
        ),
        label='Nome da bomba'
    )

    tanque = forms.ModelChoiceField(required=False,
        queryset=Tanque.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form__input'
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
            self.fields['tanque'].queryset = Tanque.objects.filter(empresa=self.empresa)

    
    def clean_nome_bomba(self):
        nome_bomba = self.cleaned_data.get('nome_bomba')

        if not self.empresa:
            raise forms.ValidationError('Empresa não informada para validação')
        
        if Bomba.objects.filter(
            nome_bomba=nome_bomba, 
            empresa=self.empresa).exclude(
                id=self.instance.pk
            ).exists():
            raise forms.ValidationError('Há uma bomba cadastrada com esse nome para esta empresa.')
        return nome_bomba
    
    def clean_tanque(self):
        tanque = self.cleaned_data.get('tanque')

        if tanque and not tanque.ativo:
            raise forms.ValidationError('Esta bomba está desativada.')
        return tanque
    
    def save(self, commit=True):

        usuario = self.instance.empresa
        bomba = self.instance
        bomba.empresa = usuario
        bomba.nome_bomba = self.cleaned_data.get('nome_bomba')
        bomba.tanque = self.cleaned_data.get('tanque')
        bomba.ativo = self.cleaned_data.get('status')

        if commit:
            bomba.save()

        return bomba