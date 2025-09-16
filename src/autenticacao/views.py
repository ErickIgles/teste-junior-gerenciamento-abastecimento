from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from django.views.generic import FormView
from django.urls import reverse_lazy

from .forms import FuncionarioLoginForm, EmpresaLoginForm


class FuncionarioLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    form_class = FuncionarioLoginForm


class UsuarioLogoutView(LogoutView):
    next_page = 'autenticacao:login'

    def dispatch(self, request, *args, **kwargs):

        # logout(request)

        return super().post(request, *args, **kwargs)


class EmpresaLoginFormView(FormView):
    template_name = 'autenticacao/login_empresa.html'
    form_class = EmpresaLoginForm
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        login(self.request, form.user)
        self.request.session['empresa_id'] = form.empresa.id
        return super().form_valid(form)
