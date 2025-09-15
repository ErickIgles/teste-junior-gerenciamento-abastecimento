from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)

from cadastros.empresas.models import Empresa
from cadastros.funcionarios.models import Funcionario
from core.mixins import GroupRequiredMixin

from .models import Fornecedor
from .forms import FornecedorForm

from .utils.mixins import EmpresaFornecedorPermissionMixin


class FornecedorCadastroView(

    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):
    group_required = ['gerente_geral', 'administradores']
    model = Fornecedor
    form_class = FornecedorForm
    template_name = 'fornecedores/form_register.html'
    success_url = reverse_lazy('cadastros:fornecedores:listar')

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            kwargs['empresa'] = Empresa.objects.get(
                usuario_responsavel=usuario_logado
            )

        else:

            usuario_funcionario = Funcionario.objects.get(
                user=usuario_logado
            )

            kwargs['empresa'] = Empresa.objects.get(
                usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel
            )

        return kwargs

    def form_valid(self, form):

        messages.success(
            self.request,
            'Fornecedor cadastrado com sucesso.'
        )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            'Erro ao realizar o cadastro. Confira as informações.'
        )

        return super().form_invalid(form)

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:fornecedores:listar')


class FornecedorListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']
    model = Fornecedor
    context_object_name = 'fornecedores'
    template_name = 'fornecedores/lista.html'
    paginate_by = 6

    def get_queryset(self):

        queryset = super().get_queryset()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            queryset = queryset.filter(
                empresa__usuario_responsavel=usuario_logado
            )

        else:

            usuario = Funcionario.objects.get(
                user=self.request.user
            )

            queryset = queryset.filter(
                empresa=usuario.empresa
            )

        q = self.request.GET.get('q')

        data_inicio = self.request.GET.get('data_inicio')

        data_fim = self.request.GET.get('data_fim')

        if q:

            queryset = queryset.filter(nome_fantasia__icontains=q)

        if data_inicio:

            queryset = queryset.filter(criado__gte=data_inicio)

        if data_fim:

            queryset = queryset.filter(criado__lte=data_fim)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['fornecedores'] = self.get_queryset()

        return context


class FornecedorAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaFornecedorPermissionMixin,
    UpdateView
):
    group_required = ['gerente_geral', 'administradores']
    model = Fornecedor
    form_class = FornecedorForm
    context_object_name = 'fornecedor'
    template_name = 'fornecedores/form_update.html'
    success_url = reverse_lazy('cadastros:fornecedores:listar')

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            kwargs['empresa'] = Empresa.objects.get(
                usuario_responsavel=usuario_logado
            )

        else:

            usuario_funcionario = Funcionario.objects.get(
                user=usuario_logado
            )

            kwargs['empresa'] = Empresa.objects.get(
                usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel
            )

        return kwargs

    def form_valid(self, form):

        messages.success(
            self.request,
            f'Dados do fornecedor {form.instance.nome_fantasia} atualizado.'
        )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            'Erro ao atualizar dados. Confira as informações.'
        )

        return super().form_invalid(form)

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')
        
        if next_url:

            return next_url

        return reverse('cadastros:fornecedores:listar')


class FornecedorDeletarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaFornecedorPermissionMixin,
    DeleteView,
):
    group_required = ['gerente_geral', 'administradores']
    model = Fornecedor
    template_name = 'fornecedores/form_delete.html'
    context_object_name = 'fornecedor'
    success_url = reverse_lazy('cadastros:fornecedores:listar')

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        self.object.delete()

        messages.success(
            request,
            'Fornecedor excluído com sucesso.'
        )

        return redirect(self.get_success_url())
