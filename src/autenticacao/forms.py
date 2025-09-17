from django import forms
from django.contrib.auth import authenticate

from django.contrib.auth.forms import AuthenticationForm

from cadastros.empresas.models import Empresa
from cadastros.funcionarios.models import Funcionario


class FuncionarioLoginForm(AuthenticationForm):

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "autofocus": True,
                'class': 'form-input',
                'placeholder': 'Usuário'
            }
        ),
        label='Nome de usuário'
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(
            attrs={
                "autocomplete": "current-password",
                'class': 'form-input',
                'placeholder': 'Senha'
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get(
            'username'
        )
        password = cleaned_data.get(
            'password'
        )

        try:

            funcionario = Funcionario.objects.get(
                nome_funcionario=username
            )

        except Funcionario.DoesNotExist:

            raise forms.ValidationError(
                'Funcionário não encontrado.'
            )

        user_funcionrio = funcionario.user

        if user_funcionrio is None:
            raise forms.ValidationError(
                'Nenhum usuário associado a esse funcionário foi encontrado.'
            )

        user = authenticate(username=user_funcionrio, password=password)

        if user is None:
            raise forms.ValidationError(
                'Senha incorreta.'
            )

        self.user = user
        self.funcionario = funcionario

        return cleaned_data


class EmpresaLoginForm(forms.Form):
    cnpj = forms.CharField(
        max_length=18,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'CNPJ',
                'pattern': r'\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}',
                'inputmode': 'numeric'
            }
        ),
        label='CNPJ'
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Senha'
            }
        ),
        label='Senha'
    )

    def clean(self):
        cleaned_data = super().clean()

        cnpj = cleaned_data.get('cnpj')
        password1 = cleaned_data.get('password')

        try:
            empresa = Empresa.objects.get(
                cnpj=cnpj
            )

        except Empresa.DoesNotExist:

            raise forms.ValidationError(
                """
                Empresa não encontrada.
                """
            )

        user = empresa.usuario_responsavel

        if user is None:
            raise forms.ValidationError(
                """
                Nenhum usuário associado a essa empresa foi encontrado.
                """
            )

        user = authenticate(username=user.username, password=password1)

        if user is None:
            raise forms.ValidationError(
                'Senha incorreta.'
            )

        self.user = user
        self.empresa = empresa

        return cleaned_data
