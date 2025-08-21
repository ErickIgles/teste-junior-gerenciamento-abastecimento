from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import CreateView, ListView, UpdateView, View
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Bomba
from .forms import BombaForm, BombaUpdateForm
from core.mixins import GroupRequiredMixin

from .utils.mixins import EmpresaBombaPermissionMixin
from cadastros.empresas.models import Empresa


class BombaCadastroView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):
    group_required = ['gerente_geral', 'administradores']
    model = Bomba
    form_class = BombaForm
    template_name = 'bombas/form_register.html'
    success_url = reverse_lazy('cadastros:bombas:listar')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = Empresa.objects.get(
            usuario_responsavel=self.request.user
        )
        return kwargs


class BombaListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']
    model = Bomba
    context_object_name = 'bombas'
    template_name = 'bombas/lista.html'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(
            empresa__usuario_responsavel=self.request.user
        )
        q = self.request.GET.get('q')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(nome_bomba__icontains=q)
        if data_inicio:
            queryset = queryset.filter(criado__gte=data_inicio)
        if data_fim:
            queryset = queryset.filter(criado__lte=data_fim)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bombas'] = self.get_queryset()
        return context


class BombaAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaBombaPermissionMixin,
    UpdateView
):
    group_required = ['gerente_geral', 'administradores']
    model = Bomba
    form_class = BombaUpdateForm
    context_object_name = 'bomba'
    template_name = 'bombas/form_update.html'
    success_url = reverse_lazy('cadastros:bombas:listar')

    def get_initial(self):
        initial = super().get_initial()
        initial['status'] = self.object.ativo
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['empresa'] = Empresa.objects.get(
            usuario_responsavel=self.request.user
        )
        return kwargs


# class BombaDeletarView(
#     LoginRequiredMixin,
#     GroupRequiredMixin,
#     EmpresaBombaPermissionMixin,
#     DeleteView
# ):
#     group_required = ['gerente_geral', 'administradores']
#     model = Bomba
#     context_object_name = 'bomba'
#     template_name = 'bombas/form_delete.html'
#     success_url = reverse_lazy('cadastros:bombas:listar')


class BombaInativarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaBombaPermissionMixin,
    SingleObjectMixin,
    View
):
    group_required = ['gerente_geral', 'administradores']
    model = Bomba
    context_object_name = 'bomba'

    def get(self, request, *args, **kwargs):
        bomba = self.get_object()
        return render(request, 'bombas/form_inativar.html', {'bomba': bomba})

    def post(self, request, *args, **kwargs):
        bomba = self.get_object()
        bomba.ativo = False
        bomba.save()
        messages.success(
            request,
            f'Bomba {bomba.nome_bomba} desativada com sucesso.')
        return redirect('cadastros:bombas:listar')
