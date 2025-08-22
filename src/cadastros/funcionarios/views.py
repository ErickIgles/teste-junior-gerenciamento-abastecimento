from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, ListView, UpdateView

from django.views import View

from django.contrib import messages

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import SingleObjectMixin

from django.urls import reverse_lazy

from .models import Funcionario
from .forms import FuncionarioForm, FuncionarioUpdateForm
from cadastros.empresas.models import Empresa

from core.mixins import GroupRequiredMixin

from .utils.mixins import EmpresaPermissionMixin


class FuncionarioCadastrarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):
    group_required = ['gerente_geral', 'administradores']

    template_name = 'funcionarios/form_register.html'
    model = Funcionario
    form_class = FuncionarioForm
    success_url = reverse_lazy('home:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        usuario = Funcionario.objects.get(
            user=self.request.user
        )
        kwargs['empresa'] = get_object_or_404(
            Empresa,
            usuario_responsavel=usuario.empresa.usuario_responsavel
        )
        return kwargs

    def form_valid(self, form):
        messages.success(
            self.request,
            f"""Funcionário(a) {form.instance.nome_funcionario}
            cadastrado(a) com sucesso."""
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erro ao realizar o cadastro. Confira as informações fornecidas.'
        )
        return super().form_invalid(form)


class FuncionarioListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']

    template_name = 'funcionarios/lista.html'
    model = Funcionario
    context_object_name = 'funcionarios'

    def get_queryset(self):
        queryset = super().get_queryset()

        usuario = Funcionario.objects.get(
            user=self.request.user
        )
        queryset = queryset.select_related(
            'user',
            'cargo',
            'cargo__setor'
        ).filter(
            empresa=usuario.empresa
        )

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
        context['funcionarios'] = self.get_queryset()
        return context


class FuncionarioAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaPermissionMixin,
    UpdateView
):
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
        initial['status'] = self.object.ativo
        return initial

    def form_valid(self, form):
        messages.success(
            self.request,
            f"""Dados do(a) funcionário(a)
            {form.instance.nome_funcionario} atualizado com sucesso."""
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            """Erro ao tentar atualizar os dados.
            Confira as informações."""
        )
        return super().form_invalid(form)


class FuncionarioInativarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaPermissionMixin,
    SingleObjectMixin,
    View
):
    model = Funcionario
    group_required = ['gerente_geral', 'administradores']

    def get(self, request, *args, **kwargs):
        funcionario = self.get_object
        return render(
            request,
            'funcionarios/form_delete.html',
            {'funcionario': funcionario}
        )

    def post(self, request, *args, **kwargs):
        funcionario = self.get_object()
        funcionario.ativo = False
        funcionario.save()

        messages.success(
            request,
            f"""Funcionário(a) {funcionario.nome_funcionario}
            foi deletado(a) com sucesso."""
        )
        return redirect('cadastros:funcionarios:listar')
