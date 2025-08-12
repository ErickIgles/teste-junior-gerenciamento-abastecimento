from django import forms

from django.contrib.auth.forms import AuthenticationForm




class UserLoginForm(AuthenticationForm):
    
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": True, 'class': 'form__input'}))
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", 'class': 'form__input'}),
    )


