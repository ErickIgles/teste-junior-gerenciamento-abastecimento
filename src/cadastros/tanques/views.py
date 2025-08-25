from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin

from cadastros.funcionarios.models import Funcionario
from core.mixins import GroupRequiredMixin

from ..empresas.models import Empresa
from .forms import TanqueForm, TanqueUpdateForm
from .models import Tanque
from .utils.mixins import EmpresaPermissionTanqueMixin


class TanqueCadastroView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):
    group_required = ['gerente_geral', 'administradores']
    model = Tanque
    form_class = TanqueForm
    template_name = 'tanques/form_register.html'
    success_url = reverse_lazy('cadastros:tanques:listar')

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
        messages.success(self.request, f'Tanque {form.instance.identificador_tanque} cadastrado com sucesso.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Erro ao realizar o cadastro. Confira às informações.')
        return super().form_invalid(form)


class TanqueListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']
    model = Tanque
    context_object_name = 'tanques'
    template_name = 'tanques/lista.html'
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
                empresa__usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel
            )
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
        context['tanques'] = self.get_queryset() 
        return context


class TanqueAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaPermissionTanqueMixin,
    UpdateView
):
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

# class TanqueDeletarView(LoginRequiredMixin, GroupRequiredMixin, EmpresaPermissionTanqueMixin, DeleteView):
#     model = Tanque
#     context_object_name = 'tanque'
#     template_name = 'tanques/tanque_form_delete.html'
#     success_url = reverse_lazy('cadastros:tanques:listar')


class TanqueInativarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    SingleObjectMixin,
    EmpresaPermissionTanqueMixin,
    View
):
    group_required = ['gerente_geral', 'administradores']
    model = Tanque
    context_object_name = 'tanque'

    def get(self, request, *args, **kwargs):
        tanque = self.get_object()
        return render(
            request,
            'tanques/form_inativar.html',
            {'tanque': tanque}
        )

    def post(self, request, *args, **kwargs):
        tanque = self.get_object()
        tanque.ativo = False
        tanque.save()

        messages.success(
            request,
            f'Tanque {tanque.identificador_tanque} desativado com sucesso.'
        )
        return redirect('cadastros:tanques:listar')
