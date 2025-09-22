from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
)

from cadastros.empresas.models import Empresa
from cadastros.funcionarios.models import Funcionario
from core.mixins import GroupRequiredMixin

from .forms import BombaForm, BombaUpdateForm
from .models import Bomba
from .utils.mixins import EmpresaBombaPermissionMixin


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
            'Bomba cadastrada com sucesso.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erro ao realizar o cadastro. Confira às informações.'
        )
        return super().form_invalid(form)

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:bombas:listar')


class BombaListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']
    model = Bomba
    context_object_name = 'bombas'
    template_name = 'bombas/lista.html'
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
            queryset = queryset.filter(nome_bomba__icontains=q)
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

        form_cadastro = BombaForm(
            empresa=empresa,
        )

        bombas = self.get_queryset()

        for bomba in bombas:
            
            bomba.form_edicao = BombaUpdateForm(
                instance=bomba,
                empresa=empresa
            )

            bomba.form_edicao.fields['status'].initial = bomba.ativo


        context['page_obj'] = bombas 
        context['form'] = form_cadastro 

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
            f'Dados da bomba {form.instance.nome_bomba} atualizado.'
        )
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erro ao atualizar dados. Confira às informações.'
        )
        
        usuario_logado = self.request.user

        if usuario_logado.is_empresa():
            empresa = Empresa.objects.get(usuario_responsavel=usuario_logado)
        else:
            usuario_funcionario = Funcionario.objects.get(user=usuario_logado)
            empresa = Empresa.objects.get(
                usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel
            )

        bombas = Bomba.objects.select_related(
            'empresa'
        ).filter(
            empresa=empresa
        )

        for bomba in bombas:
            bomba.form_edicao = BombaUpdateForm(instance=bomba, empresa=empresa)
            bomba.form_edicao.fields['status'].initial = bomba.ativo

        context = {
            "page_obj": bombas,
            "form": BombaForm(empresa=empresa),
            "form_edicao_com_erros": form,
            "bomba_id_com_erro": self.object.id,
        }

        return render(self.request, "bombas/lista.html", context)

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('cadastros:bombas:listar')
