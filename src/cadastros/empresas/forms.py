from django import forms


from django.contrib.auth.models import User, Group
from .models import Empresa, Setor


class EmpresaModelForm(forms.ModelForm):
    nome_empresa = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'Nome da empresa'
            }
        ),
        label='Nome da empresa'
    )
    cnpj = forms.CharField(
        max_length=18,
        widget=forms.TextInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'CNPJ'
            }
        ),
        label='CNPJ da empresa'
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
            'nome_empresa',
            'cnpj',
            'telefone',
            'email'
        ]

    def clean_nome_empresa(self):
        nome_empresa = self.cleaned_data.get('nome_empresa')

        if Empresa.objects.filter(
            nome_empresa=nome_empresa
        ).exists():
            raise forms.ValidationError(
                'Há uma empresa cadastrada com esse nome.'
            )
        return nome_empresa

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if Empresa.objects.filter(
            email=email
        ).exists():
            raise forms.ValidationError(
                'Há uma empresa cadastrada com esse e-mail.'
            )
        return email

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'As senhas não coincidem.')
        return self.cleaned_data

    def save(self, commit=True):
        nome_empresa = self.cleaned_data.get('nome_empresa')
        cnpj = self.cleaned_data.get('cnpj')
        telefone = self.cleaned_data.get('telefone')
        email = self.cleaned_data.get('email')

        password = self.cleaned_data.get('password1')

        usuario = User.objects.create_user(
            username=nome_empresa,
            email=email,
            password=password
        )
        empresa = Empresa(
            nome_empresa=nome_empresa,
            cnpj=cnpj,
            telefone=telefone,
            email=email
        )

        if commit:
            empresa.usuario_responsavel = usuario
            empresa.grupo = Group.objects.get(name='administradores')
            empresa.save()

        return usuario


class EmpresaUpdateModelForm(forms.ModelForm):

    nome_empresa = forms.CharField(
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
            'nome_empresa',
            'telefone',
            'email'
        ]

    def clean_nome_empresa(self):

        nome_empresa = self.cleaned_data.get('nome_empresa')

        usuario_id = self.instance.pk

        empresa = Empresa.objects.filter(
            nome_empresa=nome_empresa
        ).exclude(
            pk=usuario_id
        )

        if empresa.exists():
            raise forms.ValidationError(
                'Não é possível utilizar esse nome de empresa.'
            )

        return nome_empresa

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

        usuario.username = self.cleaned_data.get('nome_empresa')

        usuario.email = self.cleaned_data.get('email')

        usuario.telefone = self.cleaned_data.get('telefone')

        empresa = self.instance

        empresa.nome_empresa = self.cleaned_data.get('nome_empresa')

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
