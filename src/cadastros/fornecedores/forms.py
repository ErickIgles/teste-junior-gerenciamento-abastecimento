from django import forms
from .models import Fornecedor

from .models import Fornecedor


class FornecedorForm(forms.ModelForm):

    razao_social = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Razão Social'
            }
        ),
        label='Razão Social',
        required=True
    )

    nome_fantasia = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Nome Fantasia'
            }
        ),
        label='Nome Fantasia',
        required=True
    )

    cnpj = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'CNPJ'
            }
        ),
        label='CNPJ',
        required=True
    )

    contato_principal = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Pessoa de Contato'
            }
        ),
        label='Pessoa de Contato',
        required=False
    )

    telefone = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Telefone'
            }
        ),
        label='Telefone',
        required=False
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'E-mail'
            }
        ),
        label='E-mail',
        required=False
    )

    endereco = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Endereço Completo'
            }
        ),
        label='Endereço',
        required=False
    )

    observacoes = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'class': 'form-input',
                'placeholder': 'Observações'
            }
        ),
        label='Observações',
        required=False
    )

    class Meta:
        model = Fornecedor
        fields = [
            'razao_social',
            'nome_fantasia',
            'cnpj',
            'contato_principal',
            'telefone',
            'email',
            'endereco',
            'observacoes'
        ]

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

    def clean_cnpj(self):

        cnpj = self.cleaned_data.get('cnpj')

        cnpj_numeros = ''.join(filter(str.isdigit, cnpj))

        if len(cnpj_numeros) != 14:
            raise forms.ValidationError(

                "CNPJ inválido. Ele deve ter 14 dígitos."
            )

        if self.instance.pk is None:

            fornecedor = Fornecedor.objects.select_related(
                'empresa', 'cnpj', 'email'
            ).filter(
                cnpj=cnpj,
                empresa=self.empresa
            )

            if fornecedor.exists():

                raise forms.ValidationError(

                    """
                    Já existe um fornecedor cadastrado
                    com este CNPJ para sua empresa.
                    """
                )

        return cnpj

    def clean_email(self):

        email = self.cleaned_data.get('email')

        if email and self.instance.pk is None:

            fornecedor = Fornecedor.objects.select_related(
                'empresa', 'email', 'cnpj'
            ).filter(
                email=email,
                empresa=self.empresa
            )

            if fornecedor.exists():

                raise forms.ValidationError(

                    "Já existe um fornecedor com este e-mail para sua empresa."
                )

        return email

    def clean(self):

        cleaned_data = super().clean()

        contato_principal = cleaned_data.get('contato_principal')

        telefone = cleaned_data.get('telefone')

        email = cleaned_data.get('email')

        if not any([contato_principal, telefone, email]):

            raise forms.ValidationError(

                """
                Pelo menos um dos campos de contato
                (Contato Principal, Telefone ou E-mail) deve ser preenchido.
                """

            )

        return cleaned_data

    def save(self, commit=True):

        fornecedor = super().save(commit=False)

        if self.empresa:
            fornecedor.empresa = self.empresa

        if commit:
            fornecedor.save()

        return fornecedor
