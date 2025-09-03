from django import forms

from django.contrib.auth.models import User, Group

from .models import Funcionario
from cadastros.empresas.models import Cargo, Setor


class FuncionarioForm(forms.ModelForm):

    email = forms.EmailField(
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
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'placeholder': 'Grupo do funcionário'
            }
        ),
        label='Grupo do funcionário'
    )
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'placeholder': 'Cargo'
            }
        ),
        label='Cargo do funcionário'
    )
    setor = forms.ModelChoiceField(
        queryset=Setor.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'placeholder': 'Setor'
            }
        ),
        label='Setor do funcionário'
    )

    class Meta:
        model = Funcionario
        fields = ['nome_funcionario', 'cargo']

        widgets = {
            'nome_funcionario': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Nome do Funcionário'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if self.empresa:
            self.fields['cargo'].queryset = Cargo.objects.filter(
                empresa=self.empresa
            )
            self.fields['setor'].queryset = Setor.objects.filter(
                empresa=self.empresa
            )

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error(
                'password2',
                'As senhas não coincidem.'
            )
        return self.cleaned_data

    def clean_nome_funcionario(self):
        nome_funcionario = self.cleaned_data.get('nome_funcionario')

        nome_usuario_existe = User.objects.filter(
            username=nome_funcionario
        )

        if nome_usuario_existe.exists():

            raise forms.ValidationError(
                'Este nome de usuário não pode ser utilizado.'
            )

        return nome_funcionario

    def clean_email(self):
        email = self.cleaned_data.get('email')

        email_existe = User.objects.filter(
            email=email
        )
        if email_existe.exists():

            raise forms.ValidationError(
                'Este e-mail de usuário não pode ser utilizado.'
            )

        return email

    def save(self, commit=True):

        usuario = User.objects.create_user(
            username=self.cleaned_data.get('nome_funcionario'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password1')
        )

        funcionario = Funcionario(
            nome_funcionario=self.cleaned_data.get('nome_funcionario'),
            user=usuario,
            cargo=self.cleaned_data.get('cargo'),
            empresa=self.empresa
        )
        if commit:
            funcionario.save()

            usuario_grupo = self.cleaned_data.get('grupo')
            usuario.groups.clear()
            usuario.groups.add(usuario_grupo)
            usuario.save()

        return funcionario


class FuncionarioUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-input',
                'placeholder': 'E-mail'
            }
        ),
        label='E-mail'
    )
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'placeholder': 'Grupo do funcionário'
            }
        ),
        label='Grupo do funcionário'
    )
    cargo = forms.ModelChoiceField(
        queryset=Cargo.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'placeholder': 'Cargo'
            }
        ),
        label='Cargo do funcionário'
    )
    setor = forms.ModelChoiceField(
        queryset=Setor.objects.none(),
        widget=forms.Select(
            attrs={
                'class': 'form-input',
                'placeholder': 'Setor'
            }
        ),
        label='Setor do funcionário'
    )

    status = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'checkbox'
            }
        ),
        label='Status do funcionário'
    )

    class Meta:
        model = Funcionario
        fields = [
            'nome_funcionario',
            'cargo',
            'setor',
            'email'
        ]

        widgets = {
            'nome_funcionario': forms.TextInput(
                attrs={
                    'class': 'form-input',
                    'placeholder': 'Nome do Funcionário'
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        self.empresa = kwargs.pop('empresa', None)
        super().__init__(*args, **kwargs)
        if self.empresa:
            self.fields['cargo'].queryset = Cargo.objects.filter(
                empresa=self.empresa
            )
            self.fields['setor'].queryset = Setor.objects.filter(
                empresa=self.empresa
            )

    def clean_nome_funcionario(self):
        nome_funcionario = self.cleaned_data.get('nome_funcionario')
        user_id = self.instance.user.pk

        nome_user = User.objects.filter(
            username=nome_funcionario
        ).exclude(
            pk=user_id
        )

        if nome_user.exists():
            raise forms.ValidationError(
                'Este nome de usuário não pode ser utilizado.'
            )
        return nome_funcionario

    def clean_email(self):

        email = self.cleaned_data.get('email')

        user_id = self.instance.user.pk

        email_existente = User.objects.filter(
            email=email
        ).exclude(
            pk=user_id
        )

        if email_existente.exists():

            raise forms.ValidationError('Este e-mail não pode ser utilizado.')

        return email

    def save(self, commit=True):

        usuario = self.instance.user

        usuario.username = self.cleaned_data.get('nome_funcionario')

        usuario.email = self.cleaned_data.get('email')

        status = self.cleaned_data.get('status')

        funcionario = self.instance

        funcionario.nome_funcionario = self.cleaned_data.get(
            'nome_funcionario'
        )

        funcionario.cargo = self.cleaned_data.get('cargo')

        funcionario.user = usuario

        funcionario.ativo = status

        if commit:

            usuario.save()

            funcionario.save()

            grupo = self.cleaned_data.get('grupo')

            if grupo:

                usuario.groups.clear()

                usuario.groups.add(grupo)

        return funcionario
