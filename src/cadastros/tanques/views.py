from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)

from cadastros.funcionarios.models import Funcionario
from core.mixins import GroupRequiredMixin

from ..empresas.models import Empresa
from .forms import (
    TanqueForm,
    TanqueUpdateForm,

    CombustivelForm
)
from .models import Tanque, Combustivel
from .utils.mixins import (
    EmpresaTanquePermissionMixin,
    EmpresaCombustivelPermissionMixin
)


class TanqueCadastroView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):
    group_required = ['gerente_geral', 'administradores']
    model = Tanque
    form_class = TanqueForm
    template_name = 'tanques/form_register.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            kwargs['empresa'] = Empresa.objects.get(

                usuario_responsavel=self.request.user
            )

        else:

            usuario_funcionario = Funcionario.objects.get(

                user=usuario_logado
            )

            kwargs['empresa'] = Empresa.objects.get(

                usuario_responsavel = usuario_funcionario.empresa.usuario_responsavel
            )
        return kwargs

    def form_valid(self, form):

        messages.success(self.request,
                        f"""Tanque
                        {form.instance.identificador_tanque}
                        cadastrado com sucesso.""")

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(self.request,
                       """ Erro ao realizar o cadastro.
                       Confira às informações."""
                       )

        return super().form_invalid(form)

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:tanques:listar')


class TanqueListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']
    model = Tanque
    context_object_name = 'tanques'
    template_name = 'tanques/lista.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            empresa = Empresa.objects.get(
                usuario_responsavel=usuario_logado
            )

            queryset = queryset.filter(
                empresa=empresa
            )

        else:

            funcionario = Funcionario.objects.get(
                user=usuario_logado
            )

            empresa = Empresa.objects.get(
                usuario_responsavel=funcionario.empresa.usuario_responsavel
            )

            queryset = queryset.filter(
                empresa__usuario_responsavel=empresa
            )

        q = self.request.GET.get("q")

        data_inicio = self.request.GET.get('data_inicio')

        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(

                Q(tipo_combustivel__nome_combustivel__icontains=q) |

                Q(identificador_tanque__icontains=q) |

                Q(capacidade_maxima__icontains=q) |

                Q(ativo__icontains=q)
            )

        if data_inicio:

            queryset = queryset.filter(criado__gte=data_inicio)

        if data_fim:

            queryset = queryset.filter(criado__lte=data_fim)    

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['tanques'] = self.get_queryset()

        return context


class TanqueAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaTanquePermissionMixin,
    UpdateView
):
    group_required = ['gerente_geral', 'administradores']

    model = Tanque
    form_class = TanqueUpdateForm
    context_object_name = 'tanque'
    template_name = 'tanques/form_update.html'

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:tanques:listar')

    def get_initial(self):

        initial = super().get_initial()

        initial['status'] = self.object.ativo

        return initial

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            kwargs['empresa'] = Empresa.objects.get(

                usuario_responsavel=self.request.user
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
            'Tanque atualizado com sucesso.'
            )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            """Erro ao atualizar o Tanque.
                Confira às informações"""
        )

        return super().form_invalid(form)


class CombustivelCadastroView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):

    template_name = 'combustiveis/form_register.html'
    model = Combustivel
    form_class = CombustivelForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            kwargs['empresa'] = Empresa.objects.get(

                usuario_responsavel=self.request.user
            )

        else:

            usuario_funcionario = Funcionario.objects.get(

                user=usuario_logado
            )

            kwargs['empresa'] = Empresa.objects.get(

                usuario_responsavel = usuario_funcionario.empresa.usuario_responsavel
            )
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Combustível cadastrado com sucesso.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, """
        Erro ao realizar o cadastro. Confira às informações.
        """)
        return super().form_invalid(form)
    
    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:tanques:listar_combustivel')


class CombustivelListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']
    model = Combustivel
    template_name = 'combustiveis/lista.html'
    paginate_by = 6

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
                empresa__usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel
            )

        q = self.request.GET.get("q")

        data_inicio = self.request.GET.get('data_inicio')

        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(
                Q(nome_combustivel__icontains=q)
            )

        if data_inicio:

            queryset = queryset.filter(criado__gte=data_inicio)

        if data_fim:

            queryset = queryset.filter(criado__lte=data_fim)    

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['combustivel'] = self.get_queryset()

        return context


class CombustivelAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaCombustivelPermissionMixin,
    UpdateView,
):
    group_required = ['gerente_geral', 'administradores']
    model = Combustivel
    form_class = CombustivelForm
    context_object_name = 'combustivel'
    template_name = 'combustiveis/form_update.html'

    def get_form_kwargs(self):

        kwargs = super().get_form_kwargs()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            kwargs['empresa'] = Empresa.objects.get(

                usuario_responsavel=self.request.user
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
            'Combustível atualizado com sucesso.'
            )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            """Erro ao atualizar o .
                Confira às informações"""
        )

        return super().form_invalid(form)

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:tanques:listar_combustivel')


class CombustivelDeletarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaCombustivelPermissionMixin,
    DeleteView
):
    group_required = ['gerente_geral', 'administradores']

    model = Combustivel
    template_name = 'combustiveis/form_delete.html'
    context_object_name = 'combustivel'

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        try:
            return super().delete(request, *args, **kwargs)

        except ProtectedError:
            messages.error(
                request,
                'Este combustível não pode ser excluído porque já foi usado em abastecimento.'
            )
            return redirect(self.get_success_url())

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:tanques:listar_combustivel')
