from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import RegistroAbastecimento
from .forms import AbastecimentoForm, AbastecimentoUpdateForm

from core.mixins import GroupRequiredMixin
from cadastros.funcionarios.models import Funcionario
from cadastros.empresas.models import Empresa
from .utils.mixins import EmpresaAbastecimentoPermissionMixin


class RegistroAbastecimentoCadastroView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):
    group_required = ['gerente_geral', 'administradores']
    model = RegistroAbastecimento
    form_class = AbastecimentoForm
    template_name = 'abastecimento/form_register.html'
    success_url = reverse_lazy('cadastros:abastecimento:listar')

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
            kwargs['usuario_funcionario'] = usuario_logado
        return kwargs

    def form_valid(self, form):
        messages.success(
            self.request,
            'Registro cadastrado com sucesso.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erro ao realizar o cadastro. Confira às informações.'
        )
        return super().form_invalid(form)


class RegitroAbastecimentoListaView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']
    model = RegistroAbastecimento
    context_object_name = 'abastecimentos'
    template_name = 'abastecimento/lista.html'
    paginate_by = 9

    def get_queryset(self):

        queryset = super().get_queryset()
        usuario_logado = self.request.user

        if usuario_logado.is_empresa():
            queryset = queryset.filter(
                empresa__usuario_responsavel=usuario_logado
            )

        else:
            usuario_funcionario = Funcionario.objects.get(
                user=usuario_logado
            )
            queryset = queryset.filter(
                empresa=usuario_funcionario.empresa
            )

        q = self.request.GET.get('q')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(bomba__nome_bomba__icontains=q)
        if data_inicio:
            queryset = queryset.filter(criado__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(criado__lte=data_fim)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RegistroAbastecimentoAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaAbastecimentoPermissionMixin,
    UpdateView
):
    group_required = ['gerente_geral', 'administradores']
    model = RegistroAbastecimento
    form_class = AbastecimentoUpdateForm
    context_object_name = 'abastecimento'
    template_name = 'abastecimento/form_update.html'
    success_url = reverse_lazy('cadastros:abastecimento:listar')

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
            kwargs['usuario_funcionario'] = usuario_logado
        return kwargs

    def form_valid(self, form):
        messages.success(
            self.request,
            'Dados atualizados com suceso.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erro ao atualizar os dados. Confira às informações.'
        )
        return super().form_invalid(form)


class RegistroAbastecimentoDeletarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaAbastecimentoPermissionMixin,
    DeleteView
):
    group_required = ['gerente_geral', 'administradores']
    model = RegistroAbastecimento
    context_object_name = 'abastecimento'
    template_name = 'abastecimento/form_delete.html'
    success_url = reverse_lazy('cadastros:abastecimento:listar')
