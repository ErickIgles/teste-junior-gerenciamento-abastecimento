from django import forms

from django.contrib.auth.models import User

from .models import Funcionario


class FuncionarioForm(forms.ModelForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form__input', 'placeholder': 'E-mail'}), label='E-mail')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': 'Senha'}), label='Senha')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': 'Confirmação de senha'}), label='Confirmação de Senha')

    class Meta:
        model = Funcionario
        fields = ['nome_funcionario', 'cargo', 'setor']

        widgets = {
            'nome_funcionario': forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Nome do Funcionário'}),
            'cargo': forms.Select(attrs={'class': 'form__input'}),
            'setor': forms.Select(attrs={'class': 'form__input'})
        }
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'As senhas não coincidem.')
        return self.cleaned_data
    
    def clean_nome_funcionario(self):
        nome_funcionario = self.cleaned_data.get('nome_funcionario')
        if User.objects.filter(username=nome_funcionario).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return nome_funcionario
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email

    def save(self, commit=True):

        nome_funcionario = self.cleaned_data.get('nome_funcionario')
        password1 = self.cleaned_data.get('password1')
        email = self.cleaned_data.get('email')

        setor = self.cleaned_data.get('setor')
        cargo = self.cleaned_data.get('cargo')

        user = User.objects.create_user(username=nome_funcionario, email=email, password=password1)

        funcionario = Funcionario(nome_funcionario=nome_funcionario, user=user, cargo=cargo, setor=setor)
        if commit:
            funcionario.save()
        return funcionario

