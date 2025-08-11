from django.contrib.auth.models import User
from django.views.generic import CreateView

from django.urls import reverse_lazy
from .forms import UserForm



class FuncionarioCadastrarView(CreateView):
    template_name = 'funcionarios/form_register.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)

