
import re
from django.core.exceptions import ValidationError
from django import forms
from django.db import transaction

from django.contrib.auth.models import User, Group
from .models import Empresa, Setor, Cargo


class EmpresaModelForm(forms.ModelForm):
    razao_social = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Razão Social'
            }
        ),
        label='Razão Social'
    )

    nome_fantasia = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Nome Fantasia'
            }
        ),
        label='Nome Fantasia'
    )

    cnpj = forms.CharField(
        max_length=18,
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

    telefone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Telefone'
            }
        ),
        label='Telefone'
    )

    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'E-mail'
            }
        ),
        label='E-mail'
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Senha'
            }
        ),
        label='Senha'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Confirmação de senha'
            }
        ),
        label='Confirmação de Senha'
    )

    class Meta:
        model = Empresa
        fields = [
            'razao_social',
            'nome_fantasia',
            'cnpj',
            'telefone',
            'email'
        ]

    def clean_razao_social(self):
        razao_social = self.cleaned_data.get('razao_social')
        if Empresa.objects.filter(razao_social=razao_social).exists():
            raise forms.ValidationError('Já existe uma empresa com essa razão social.')
        return razao_social

    def clean_nome_fantasia(self):
        nome_fantasia = self.cleaned_data.get('nome_fantasia')
        if Empresa.objects.filter(nome_fantasia=nome_fantasia).exists():
            raise forms.ValidationError('Já existe uma empresa com esse nome fantasia.')
        return nome_fantasia

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Empresa.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe uma empresa com esse e-mail.')
        return email
    
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get('cnpj')

        cnpj_numeros = re.sub(r'\D', '', cnpj or '')

        if len(cnpj_numeros) != 14:
            raise ValidationError('CNPJ deve conter 14 dígitos.')

        if cnpj_numeros == cnpj_numeros[0] * 14:
            raise ValidationError('CNPJ inválido.')

        return cnpj

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')

        telefone_numeros = re.sub(r'\D', '', telefone or '')

        if len(telefone_numeros) not in [10, 11]:
            raise ValidationError('Telefone deve ter 10 ou 11 dígitos (com DDD).')

        padrao = r'^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$'
        if not re.match(padrao, telefone):
            raise ValidationError('Formato de telefone inválido. Ex: (85)99999-8888')

        return telefone

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        razao_social = cleaned_data.get('razao_social')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'As senhas não coincidem.')

        if User.objects.filter(username=razao_social).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')

        return cleaned_data

    def save(self, commit=True):
        
        razao_social = self.cleaned_data.get('razao_social')
        nome_fantasia = self.cleaned_data.get('nome_fantasia')
        cnpj = self.cleaned_data.get('cnpj')
        telefone = self.cleaned_data.get('telefone')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')

        with transaction.atomic():

            usuario = User.objects.create_user(
                username=razao_social,
                email=email,
                password=password
            )

            empresa = Empresa(
                razao_social=razao_social,
                nome_fantasia=nome_fantasia,
                cnpj=cnpj,
                telefone=telefone,
                email=email,
                usuario_responsavel=usuario
            )

            if commit:
                empresa.grupo = Group.objects.get(name='administradores')
                empresa.save()

        return empresa


class EmpresaUpdateModelForm(forms.ModelForm):

    razao_social = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Nome da empresa'
            }
        ),
        label='Nome da empresa'
    )
    telefone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'telefone'
            }
        ),
        label='Telefone para contato'
    )
    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'E-mail'
            }
        ),
        label='E-mail'
    )

    class Meta:
        model = Empresa
        fields = [
            'razao_social',
            'telefone',
            'email'
        ]

    def clean_razao_social(self):

        razao_social = self.cleaned_data.get('razao_social')

        usuario_id = self.instance.pk

        empresa = Empresa.objects.filter(
            razao_social=razao_social
        ).exclude(
            pk=usuario_id
        )

        if empresa.exists():
            raise forms.ValidationError(
                'Não é possível utilizar esse nome de empresa.'
            )

        return razao_social

    def clean_email(self):

        email = self.cleaned_data.get('email')

        usuario_id = self.instance.pk

        empresa = Empresa.objects.filter(
            email=email
        ).exclude(
            pk=usuario_id
        )

        if empresa.exists():
            raise forms.ValidationError('Não é possível utilizar esse e-mail.')

        return email

    def clean_telefone(self):

        telefone = self.cleaned_data.get('telefone')
        usuario_id = self.instance.pk

        empresa = Empresa.objects.filter(
            telefone=telefone
        ).exclude(
            pk=usuario_id
        )

        if empresa.exists():

            raise forms.ValidationError(
                'Não é possível utilizar este número de telefone.'
            )

        return telefone

    def save(self, commit=True):

        usuario = self.instance.usuario_responsavel

        usuario.username = self.cleaned_data.get('razao_social')

        usuario.email = self.cleaned_data.get('email')

        usuario.telefone = self.cleaned_data.get('telefone')

        empresa = self.instance

        empresa.razao_social = self.cleaned_data.get('razao_social')

        empresa.usuario_responsavel = usuario

        if commit:

            usuario.save()
            empresa.save()

        return empresa


class SetorModelForm(forms.ModelForm):

    nome_setor = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Setor'
            }
        ),
        label='Setor'
    )

    class Meta:

        model = Setor

        fields = [
            'nome_setor'
        ]

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

    def clean_nome_setor(self):

        setor = self.cleaned_data.get('nome_setor')

        if len(setor) < 5:

            self.add_error(
                'nome_setor',
                'O nome do setor não pode ser menor que 5 letras.'
            )

        return setor

    def save(self, commit=True):
        setor = super().save(commit=False)

        setor.empresa = self.empresa

        if setor:
            setor.save()

        return setor


class CargoModelForm(forms.ModelForm):

    nome_cargo = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Cargo'
            }
        ),
        label='Cargo'
    )
    setor = forms.ModelChoiceField(
        required=True,
        queryset=Setor.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        ),
        label='Setor'
    )

    class Meta:

        model = Cargo
        fields = [
            'nome_cargo',
            'setor'
        ]

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)

        if self.empresa:

            self.fields['setor'].queryset = Setor.objects.select_related(
                'empresa'
            ).filter(
                empresa=self.empresa
            )

        if self.instance and self.instance.pk:

            setor_atual = self.instance.setor

            if setor_atual and setor_atual not in self.fields['setor'].queryset:

                self.fields['setor'].queryset = Setor.objects.filter(
                    empresa=setor_atual.empresa
                )

    def clean_nome_cargo(self):

        nome_cargo = self.cleaned_data.get('nome_cargo')

        if len(nome_cargo) < 7:

            self.add_error(
                'nome_cargo',
                'O nome do cargo não pode ser menor que 7 letras'
            )

        return nome_cargo

    def save(self, commit=True):

        cargo = super().save(commit=False)

        cargo.empresa = self.empresa

        if commit:

            cargo.save()

        return cargo
