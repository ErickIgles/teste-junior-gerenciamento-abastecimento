from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic import (
    CreateView,
    UpdateView,
    ListView,
    DeleteView,
    View
)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.http import Http404

from core.mixins import GroupRequiredMixin

from cadastros.funcionarios.models import Funcionario

from .utils.mixins import (
    UserPermissionMixin,
    EmpresaPermissionMixin,
    EmpresaSetorPermissionMixin,
    EmpresaCargoPermissionMixin
)

from .models import Empresa, Setor, Cargo

from .forms import (
    EmpresaModelForm,
    EmpresaUpdateModelForm,
    SetorModelForm,
    CargoModelForm
)


class EmpresaCriarView(CreateView):
    template_name = 'empresas/form_register.html'
    form_class = EmpresaModelForm
    model = Empresa
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):

        response = super().form_valid(form)

        login(self.request, self.object)

        messages.success(
            self.request,
            'Empresa cadastrada com sucesso.'
        )

        return response

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erro ao realizar o cadastro. Confira às informações.'
        )
        return super().form_invalid(form)


class EmpresaPerfilView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaPermissionMixin,
    UpdateView
):

    group_required = ['administradores']
    model = Empresa
    form_class = EmpresaUpdateModelForm
    template_name = 'empresas/perfil.html'
    context_object_name = 'empresa'
    success_url = reverse_lazy('cadastros:empresas:perfil')

    def get_object(self, queryset=None):
        try:
            empresa = Empresa.objects.get(
                usuario_responsavel=self.request.user
            )
            return empresa
        except Empresa.DoesNotExist:
            raise Http404('Empresa não encontrada.')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Dados atualizados com sucesso.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erro ao atualizar os dados. Confira às informações.'
        )
        return super().form_invalid(form)


class EmpresaInativarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    SingleObjectMixin,
    UserPermissionMixin,
    View
):
    group_required = ['administradores']
    model = User

    def get_object(self, queryset=None):
        usuario_pk = self.kwargs.get('pk')
        return get_object_or_404(User, pk=usuario_pk)

    def get(self, request, *args, **kwargs):
        usuario = self.get_object()
        return render(
            request,
            'empresas/form_inativar.html',
            {'usuario': usuario}
        )

    def post(self, request, *args, **kwargs):

        try:
            empresa = Empresa.objects.get(
                usuario_responsavel=self.request.user
            )
            empresa.ativo = False
            empresa.save()

            usuario = self.request.user
            usuario.is_active = False
            usuario.save()
            logout(request)

        except Empresa.DoesNotExist:
            messages.error(
                request,
                'Conta e empresa desativadas com sucesso.'
            )
        except Empresa.DoesNotExist:
            messages.error(
                request,
                'Empresa não encontrada.')
            return redirect('home:index')
        except Exception as e:
            messages.error(
                request,
                f'Erro ao desativar: {str(e)}'
                )
            return redirect('home:index')

        return redirect('autenticacao:login')


class SetorCadastrarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):

    group_required = ['gerente_geral', 'administradores']
    model = Setor
    form_class = SetorModelForm
    template_name = 'setor/form_register.html'

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
            'Setor cadatrado com sucesso.'
        )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            'Erro ao realizar o cadastro. Confira às informações.'
        )

        return super().form_invalid(form)

    def get_success_url(self):

        next_url = (
            self.request.GET.get('next')
            or
            self.request.POST.get('next')
        )
        if next_url:

            return next_url

        return reverse('cadastros:empresas:listar_setor')


class SetorListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'admistradores']
    model = Setor
    template_name = 'setor/lista.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            empresa = Empresa.objects.select_related(
                'usuario_responsavel'
            ).get(
                usuario_responsavel=usuario_logado
            )

        else:

            funcionario = Funcionario.objects.select_related(
                'user'
            ).get(
                user=usuario_logado
            )

            empresa = Empresa.objects.get(
                usuario_responsavel=funcionario.empresa.usuario_responvel
            )

        queryset = queryset.filter(
            empresa=empresa
        )

        q = self.request.GET.get('q')

        data_inicio = self.request.GET.get('data_inicio')

        data_fim = self.request.GET.get('data_fim')

        if q:

            queryset = queryset.filter(
                Q(nome_setor__icontains=q)
            )

        if data_inicio:

            queryset = queryset.filter(criado__gte=data_inicio)

        if data_fim:

            queryset = queryset.filter(criado__lte=data_fim)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():
            empresa = Empresa.objects.get(usuario_responsavel=usuario_logado)
        else:
            usuario_funcionario = Funcionario.objects.get(user=usuario_logado)
            empresa = Empresa.objects.get(usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel)

        form_cadastro = SetorModelForm(
            empresa=empresa,
        )

        setores = self.get_queryset()

        for setor in setores:
            
            setor.form_edicao = SetorModelForm(
                instance=setor,
                empresa=empresa
            )


        context['page_obj'] = setores 
        context['form'] = form_cadastro 

        return context


class SetorAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaSetorPermissionMixin,
    UpdateView
):

    group_required = ['gerente_geral', 'administradores']

    model = Setor
    form_class = SetorModelForm
    template_name = 'setor/form_atualizar.html'
    context_object_name = 'setor'

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
            'Setor atualizado com sucesso.'
        )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            'Erro ao atualizar os dados. Confira às informações.'
        )

        return super().form_invalid(form)

    def get_success_url(self):

        next_url = (
            self.request.GET.get('next')
            or
            self.request.POST.get('next')
        )
        if next_url:

            return next_url

        return reverse('cadastros:empresas:listar_setor')


class SetorDeletarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaSetorPermissionMixin,
    DeleteView
):

    group_required = ['gerente_geral', 'administradores']
    model = Setor
    template_name = 'setor/form_delete.html'

    def get_success_url(self):

        next_url = (
            self.request.GET.get('next')
            or
            self.request.POST.get('next')
        )
        if next_url:

            return next_url

        return reverse('cadastros:empresas:listar_setor')


class CargoCadastrarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):

    group_required = ['gerente_geral', 'administradores']
    model = Cargo
    form_class = CargoModelForm
    template_name = 'cargo/form_register.html'

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
            'Cargo cadatrado com sucesso.'
        )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            'Erro ao realizar o cadastro. Confira às informações.'
        )

        return super().form_invalid(form)

    def get_success_url(self):

        next_url = (
            self.request.GET.get('next')
            or
            self.request.POST.get('next')
        )
        if next_url:

            return next_url

        return reverse('cadastros:empresas:listar_cargo')


class CargoListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):

    group_required = ['gerente_geral', 'administradores']
    model = Cargo
    template_name = 'cargo/lista.html'
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            empresa = Empresa.objects.select_related(
                'usuario_responsavel'
            ).get(
                usuario_responsavel=usuario_logado
            )

        else:

            funcionario = Funcionario.objects.select_related(
                'user'
            ).get(
                user=usuario_logado
            )

            empresa = Empresa.objects.get(
                usuario_responsavel=funcionario.empresa.usuario_responvel
            )

        queryset = queryset.filter(
            empresa=empresa
        )

        q = self.request.GET.get('q')

        data_inicio = self.request.GET.get('data_inicio')

        data_fim = self.request.GET.get('data_fim')

        if q:

            queryset = queryset.filter(
                Q(nome_cargo__icontains=q) |
                Q(setor__nome_setor__icontains=q)
            )

        if data_inicio:

            queryset = queryset.filter(criado__gte=data_inicio)

        if data_fim:

            queryset = queryset.filter(criado__lte=data_fim)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():
            empresa = Empresa.objects.get(usuario_responsavel=usuario_logado)
        else:
            usuario_funcionario = Funcionario.objects.get(user=usuario_logado)
            empresa = Empresa.objects.get(usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel)

        form_cadastro = CargoModelForm(
            empresa=empresa,
        )

        cargos = self.get_queryset()

        for cargo in cargos:
            
            cargo.form_edicao = CargoModelForm(
                instance=cargo,
                empresa=empresa
            )


        context['page_obj'] = cargos 
        context['form'] = form_cadastro 

        return context


class CargoAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaCargoPermissionMixin,
    UpdateView
):

    group_required = ['gerente_geral', 'administradores']
    model = Cargo
    form_class = CargoModelForm
    template_name = 'cargo/form_atualizar.html'
    context_object_name = 'cargo'

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
            'Cargo atualizado com sucesso.'
        )

        return super().form_valid(form)

    def form_invalid(self, form):

        messages.error(
            self.request,
            'Erro ao atualizar os dados. Confira às informações.'
        )

        return super().form_invalid(form)

    def get_success_url(self):

        next_url = (
            self.request.GET.get('next')
            or
            self.request.POST.get('next')
        )
        if next_url:

            return next_url

        return reverse('cadastros:empresas:listar_cargo')


class CargoDeletarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaCargoPermissionMixin,
    DeleteView
):
    group_required = ['gerente_geral', 'administradores']
    model = Cargo
    template_name = 'cargo/form_delete.html'

    def get_success_url(self):

        next_url = (
            self.request.GET.get('next')
            or
            self.request.POST.get('next')
        )
        if next_url:

            return next_url

        return reverse('cadastros:empresas:listar_cargo')
