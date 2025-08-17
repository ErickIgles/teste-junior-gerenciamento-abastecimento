from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy

from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from .models import Empresa

from .forms import EmpresaModelForm, EmpresaUpdateModelForm




class EmpresaCriarView(CreateView):
    template_name = 'empresas/empresas_form.html'
    form_class = EmpresaModelForm
    model = Empresa
    success_url = reverse_lazy('home:index')


    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)


class EmpresaAtulizarView(UpdateView):
    template_name = 'empresas/empresas_form_atualizar.html'
    form_class = EmpresaUpdateModelForm
    model = Empresa
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)


class EmpresaPerfilView(DetailView):
    model = Empresa
    template_name = 'empresas/perfil.html'
    context_object_name = 'empresa'


    def get_queryset(self):
        return Empresa.objects.filter(usuario_responsavel=self.request.user)


class EmpresaDeletarView(DeleteView):
    template_name = 'empresas/empresas_form_deletar.html'
    model = Empresa
    success_url = reverse_lazy('home:index')

    def get_queryset(self):
        return Empresa.objects.filter(usuario_responsavel=self.request.user)
    
