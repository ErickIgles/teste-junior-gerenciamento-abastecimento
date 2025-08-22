from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404

from django.contrib import messages
from django.contrib.auth import logout
from django.views.generic import CreateView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from .models import Empresa

from .forms import EmpresaModelForm, EmpresaUpdateModelForm
from core.mixins import GroupRequiredMixin
from .utils.mixins import UserPermissionMixin, EmpresaPermissionMixin
from django.contrib.auth.models import User


class EmpresaCriarView(CreateView):
    template_name = 'empresas/form_register.html'
    form_class = EmpresaModelForm
    model = Empresa
    success_url = reverse_lazy('home:index')

    def form_valid(self, form):
        messages.success(
            self.request,
            'Empresa cadastrada com sucesso.'
        )
        return super().form_valid(form)

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

    group_required = ['gerente_geral', 'administradores']
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
    group_required = ['gerente_geral', 'administradores']
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
