from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from django.contrib import messages
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy

from .models import Funcionario
from .forms import FuncionarioForm, FuncionarioUpdateForm
from django.contrib.auth.models import Group
from cadastros.empresas.models import Empresa, Cargo

from core.views import GroupRequiredMixin

from .utils.mixins import EmpresaPermissionMixin




""" OK  """
class FuncionarioCadastrarView(LoginRequiredMixin, GroupRequiredMixin, CreateView):
    group_required = ['gerente_geral', 'administradores']

    template_name = 'funcionarios/form_register.html'
    model = Funcionario
    form_class = FuncionarioForm
    success_url = reverse_lazy('home:index')


    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        try:
            empresa = Empresa.objects.get(usuario_responsavel=self.request.user)
        except Empresa.DoesNotExist:
           return redirect('home:index')
        
        form.fields['cargo'].queryset = Cargo.objects.filter(setor__empresa=empresa)
        return form
       
    def form_valid(self, form):
        messages.success(self.request, f'Funcionário(a) {form.instance.nome_funcionario} cadastrado(a) com sucesso.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao realizar o cadastro. Confira as informações fornecidas.')
        return super().form_invalid(form)

""" OK """
class FuncionarioListarView(LoginRequiredMixin, GroupRequiredMixin, ListView):
    group_required = ['gerente_geral', 'administradores']

    template_name = 'funcionarios/lista_funcionario.html'
    model = Funcionario
    context_object_name = 'funcionarios'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(cargo__setor__empresa__usuario_responsavel=self.request.user)
        q = self.request.GET.get('q')
        
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(nome_funcionario__icontains=q)
        if data_inicio:
            queryset = queryset.filter(criado__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(criado__lte=data_fim)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        lista_objetos = context.get('object_list')
        pagination = Paginator(lista_objetos, 2)

        page_number = self.request.GET.get('page')
        page_obj = pagination.get_page(page_number)
        context['page_obj'] = page_obj
        return context
    
""" ok """
class FuncionarioAtualizarView(LoginRequiredMixin, GroupRequiredMixin, EmpresaPermissionMixin, UpdateView):
    group_required = ['gerente_geral', 'administradores']

    template_name = 'funcionarios/form_update.html'
    model = Funcionario
    context_object_name = 'funcionario'
    form_class = FuncionarioUpdateForm
    success_url = reverse_lazy('cadastros:funcionarios:listar')

    def get_initial(self):
        initial = super().get_initial()

        funcionario = self.get_object()
        grupo = funcionario.user.groups.all()

        initial['email'] = self.object.user.email
        initial['grupo'] = grupo.first()
        return initial

    def form_valid(self, form):
        messages.success(self.request, f'Dados do(a) funcionário(a) {form.instance.nome_funcionario} atualizado com sucesso.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, f'Erro ao tentar atualizar os dados. Confira as informações.')
        return super().form_invalid(form)

""" Ok """
class FuncionarioDeletarView(LoginRequiredMixin, GroupRequiredMixin, EmpresaPermissionMixin, DeleteView):
    template_name = 'funcionarios/form_delete.html'
    model = Funcionario
    success_url = reverse_lazy('cadastros:funcionarios:listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        funcionario = self.get_object()
        if funcionario:
            context['funcionario'] = funcionario
        return context

    def delete(self, request, *args, **kwargs):
        funcionario = self.get_object()
        nome_funcionario = funcionario.nome_funcionario
        messages.success(request, f'Funcionário(a) {nome_funcionario} deletado(a) com sucesso.')
        return super().delete(request, *args, **kwargs)

