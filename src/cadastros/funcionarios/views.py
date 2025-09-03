from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView

from cadastros.empresas.models import Empresa
from core.mixins import GroupRequiredMixin

from .forms import FuncionarioForm, FuncionarioUpdateForm
from .models import Funcionario
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

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():
            kwargs['empresa'] = get_object_or_404(
                Empresa,
                usuario_responsavel=usuario_logado
            )

        else:
            usuario_funcionario = Funcionario.objects.get(
                user=self.request.user
            )

            kwargs['empresa'] = get_object_or_404(
                Empresa,
                usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel
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

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:funcionarios:listar')


class FuncionarioListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']

    template_name = 'funcionarios/lista.html'
    model = Funcionario
    context_object_name = 'funcionarios'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            queryset = Funcionario.objects.filter(
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
            queryset = queryset.filter(

                Q(nome_funcionario__icontains=q) |

                Q(cargo__nome_cargo__icontains=q) |

                Q(setor__nome_setor__icontains=q)
            )
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
        initial['setor'] = self.object.setor
        initial['cargo'] = self.object.cargo
        initial['status'] = self.object.ativo
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():
            kwargs['empresa'] = get_object_or_404(
                Empresa,
                usuario_responsavel=usuario_logado
            )

        else:
            usuario_funcionario = Funcionario.objects.get(
                user=self.request.user
            )

            kwargs['empresa'] = get_object_or_404(
                Empresa,
                usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel
            )
        return kwargs

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

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:funcionarios:listar')
