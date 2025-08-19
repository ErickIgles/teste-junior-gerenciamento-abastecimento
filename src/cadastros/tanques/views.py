from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from django.views.generic import CreateView, ListView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin


from .models import Tanque
from .forms import TanqueForm, TanqueUpdateForm
from core.mixins import GroupRequiredMixin
from ..empresas.models import Empresa
from .utils.mixins import EmpresaPermissionTanqueMixin

from django.contrib import messages

class TanqueCadastroView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = ['gerente_geral', 'administradores']
    model = Tanque
    form_class = TanqueForm
    template_name = 'tanques/form_register.html'
    success_url = reverse_lazy('cadastros:tanques:listar')

    def form_valid(self, form):

        usuario = self.request.user

        try:
            empresa = usuario.cargo.setor.empresa
            form.instance.empresa = empresa

        except Empresa.DoesNotExist:
            form.add_error(None, "Empresa não encontrada para este usuário.")
            return self.form_invalid(form)
        
        messages.success(self.request, f'Tanque {form.instance.identificador_tanque} cadastrado com sucesso.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao realizar o cadastro. Confira às informações.')
        return super().form_invalid(form)


class TanqueListarView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = ['gerente_geral', 'administradores']
    model = Tanque
    context_object_name = 'tanques'
    template_name = 'tanques/lista.html'


    def get_queryset(self):
        queryset = super().get_queryset()
        q = self.request.GET.get("q")
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(tipo_combustivel__icontains=q)
        if data_inicio:
            queryset = queryset.filter(criado__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(criado__lte=data_fim)    
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_objetos = context.get('object_list')
        paginator = Paginator(lista_objetos, 2)

        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        return context


class TanqueAtualizarView(LoginRequiredMixin, GroupRequiredMixin, EmpresaPermissionTanqueMixin, UpdateView):
    group_required = ['gerente_geral', 'administradores']

    model = Tanque
    form_class = TanqueUpdateForm
    context_object_name = 'tanque'
    template_name = 'tanques/form_update.html'
    success_url = reverse_lazy('cadastros:tanques:listar')


    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = self.object.ativo
        return initial


# class TanqueDeletarView(LoginRequiredMixin, GroupRequiredMixin, EmpresaPermissionTanqueMixin, DeleteView):
#     model = Tanque
#     context_object_name = 'tanque'
#     template_name = 'tanques/tanque_form_delete.html'
#     success_url = reverse_lazy('cadastros:tanques:listar')    


class TanqueInativarView(LoginRequiredMixin, GroupRequiredMixin, SingleObjectMixin, EmpresaPermissionTanqueMixin, View):
    group_required = ['gerente_geral', 'administradores']
    model = Tanque


    def get(self, request, *args, **kwargs):
        tanque = self.get_object()
        return render(request, 'tanques/form_inativar.html', {'tanque': tanque})
    
    def post(self, request, *args, **kwargs):
        tanque = self.get_object()
        tanque.ativo = False
        tanque.save()

        messages.success(request, f'Tanque {tanque.identificador_tanque} desativado com sucesso.')
        return redirect('cadastros:tanques:listar')
