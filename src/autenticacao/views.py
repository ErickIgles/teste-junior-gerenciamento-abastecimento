from django.shortcuts import render

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserLoginForm


class UsuarioLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    form_class = UserLoginForm

    
class UsuarioLogoutView(LogoutView):
    next_page = 'home:index'

