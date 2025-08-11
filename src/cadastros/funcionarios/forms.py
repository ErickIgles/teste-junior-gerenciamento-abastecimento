from django import forms

from django.contrib.auth.models import User

from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail' ,widget=forms.EmailInput(attrs={'class': 'form__input', 'placeholder': 'E-mail'}))
    
    username = forms.CharField(label='Nome de usuário',
        widget=forms.TextInput(attrs={'class': 'form__input', 'placeholder': 'Nome de usuário'})
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': 'Senha'})
    )
    password2 = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(attrs={'class': 'form__input', 'placeholder': 'Confirme a senha'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('E-mail já cadastrado.')
        return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        required=True, 
        label='E-mail', 
        widget=forms.EmailInput(
            attrs={'class': 'form__input', 'placehold':'E-mail'}
            )
        )
    username = forms.CharField(
        label='Nome de usuário',
        widget=forms.TextInput(attrs={
            'class': 'form__input', 'placehold':'Nome de usuário'
        }))
    
    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id

        if User.objects.filter(email=email).exclude(pk=user_id).exists():
            raise forms.ValidationError('Este e-mail já está em uso.')
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.id

        if User.objects.filter(username=username).exclude(pk=user_id).exists():
            raise forms.ValidationError('Este nome de usuário já está em uso.')
        return username
