from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import (
    CreateView,
    ListView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.core.exceptions import ValidationError

from .models import RegistroAbastecimento, RegistroReabastecimento
from .forms import (
    AbastecimentoForm,
    AbastecimentoUpdateForm,
    ReabastecimentoTanqueForm
)

from core.mixins import GroupRequiredMixin
from cadastros.funcionarios.models import Funcionario
from cadastros.empresas.models import Empresa

from .utils.mixins import EmpresaAbastecimentoPermissionMixin


class RegistroAbastecimentoCadastroView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):
    group_required = ['funcionarios', 'gerente_geral', 'administradores']
    model = RegistroAbastecimento
    form_class = AbastecimentoForm
    template_name = 'abastecimento/lista.html'
    success_url = reverse_lazy('servicos:abastecimento:listar')

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

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('servicos:abastecimento:listar')


class RegistroAbastecimentoListaView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['funcionarios', 'gerente_geral', 'administradores']
    model = RegistroAbastecimento
    context_object_name = 'abastecimentos'
    template_name = 'abastecimento/lista.html'
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
                empresa=usuario_funcionario.empresa
            )

        q = self.request.GET.get('q')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(

                Q(bomba__nome_bomba__icontains=q) |

                Q(tanque__identificador_tanque__icontains=q) |

                Q(tipo_combustivel__nome_combustivel__icontains=q) |

                Q(funcionario__nome_funcionario__icontains=q)
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
            usuario_funcionario = None
        else:
            usuario_funcionario = Funcionario.objects.get(user=usuario_logado)
            empresa = Empresa.objects.get(usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel)

        form = AbastecimentoForm(
            empresa=empresa,
            usuario_funcionario=usuario_funcionario
        )

        context['form'] = form

        abastecimentos = self.get_queryset()


        page_obj = context['page_obj']  # já vem do ListView

        forms_edicao = [
            (abastecimento, AbastecimentoForm(
                instance=abastecimento,
                empresa=empresa,
                usuario_funcionario=usuario_funcionario
            ))
            for abastecimento in page_obj.object_list
        ]
        context['forms_edicao'] = forms_edicao
            
        total_listros = context['abastecimentos'].aggregate(
            total=Sum('litros_abastecido')
        )['total'] or 0

        total_valor = context['abastecimentos'].aggregate(
            total=Sum('valor_total_abastecimento')
        )['total'] or 0

        combustivel_mais_pedido = (
            abastecimentos
            .values('tipo_combustivel__nome_combustivel')
            .annotate(total=Count('id'))
            .order_by('-total')
            .first()
        )

        context['combustivel_mais_pedido'] = combustivel_mais_pedido

        context['total_litros'] = total_listros
        context['total_valor'] = total_valor

        return context


class RegistroAbastecimentoAtualizarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaAbastecimentoPermissionMixin,
    UpdateView
):
    group_required = ['funcionarios','gerente_geral', 'administradores']
    model = RegistroAbastecimento
    form_class = AbastecimentoUpdateForm
    context_object_name = 'abastecimento'
    template_name = 'abastecimento/form_update.html'
    success_url = reverse_lazy('servicos:abastecimento:listar')

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
        try:
            form.save()
            messages.success(
                self.request,
                'Dados atualizados com suceso.'
            )
            return super().form_valid(form)

        except ValidationError as error:
            messages.error(self.request, str(error))
            return self.form_invalid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Erro ao atualizar os dados. Confira às informações.'
        )
        return super().form_invalid(form)

    def get_success_url(self):

        next_url = self.request.GET.get('next') or self.request.POST.get('next')

        if next_url:

            return next_url

        return reverse('servicos:abastecimento:listar')


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
    success_url = reverse_lazy('servicos:abastecimento:listar')


class RegistroReabastecimentoCadastrarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    CreateView
):
    group_required = ['gerente_geral', 'administradores']
    model = RegistroReabastecimento
    form_class = ReabastecimentoTanqueForm
    template_name = 'reabastecimento/form_register.html'
    success_url = reverse_lazy('servicos:abastecimento:listar_reabastecimento')

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

        self.request.session['abastecimento_tanque_form'] = {
            'tanque_id': form.cleaned_data['tanque'].id,
            'quantidade': str(form.cleaned_data['quantidade']),
            'fornecedor_id': form.cleaned_data['fornecedor'].id
        }

        next_url = self.request.POST.get('next')

        self.request.session['next'] = next_url

        return redirect(
            'servicos:abastecimento:validacao_token_cadastrar_reabastecimento'
        )

    def form_invalid(self, form):

        messages.error(
            self.request,
            'Erro ao realizar o cadastro. Confira às informações.'
        )

        return super().form_invalid(form)


class RegistroReabastecimentoListarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):

    group_required = ['gerente_geral', 'administradores']
    model = RegistroReabastecimento
    context_object_name = 'reabastecimentos'
    template_name = 'reabastecimento/lista.html'
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
                empresa=usuario_funcionario.empresa
            )

        q = self.request.GET.get('q')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        if q:
            queryset = queryset.filter(

                Q(tanque__identificador_tanque__icontains=q) |

                Q(tanque__tipo_combustivel__nome_combustivel__icontains=q)
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
            usuario_funcionario = None
        else:
            usuario_funcionario = Funcionario.objects.get(user=usuario_logado)
            empresa = Empresa.objects.get(usuario_responsavel=usuario_funcionario.empresa.usuario_responsavel)

        form = ReabastecimentoTanqueForm(
            empresa=empresa,
            usuario_funcionario=usuario_funcionario
        )

        context['form'] = form


        reabastecimentos = self.get_queryset()

        context['reabastecimentos'] = reabastecimentos

        forms_edicao = [
            (reabastecimento, ReabastecimentoTanqueForm(
                instance=reabastecimento,
                empresa=empresa,
                usuario_funcionario=usuario_funcionario
            ))
            for reabastecimento in context['reabastecimentos']
        ]
        context['forms_edicao'] = forms_edicao
            
        total_listros = context['reabastecimentos'].aggregate(
            total=Sum('quantidade')
        )['total'] or 0

        total_valor = context['reabastecimentos'].aggregate(
            total=Sum('valor_total_reabastecimento')
        )['total'] or 0

        combustivel_mais_reabastecido = (
            reabastecimentos
            .values('tanque__tipo_combustivel__nome_combustivel')
            .annotate(total=Count('id'))
            .order_by('-total')
            .first()
        )

        context['combustivel_mais_reabastecido'] = combustivel_mais_reabastecido

        context['total_litros'] = total_listros
        context['total_valor'] = total_valor

        return context

class RegistroReabastecimentoDeletarView(
    LoginRequiredMixin,
    GroupRequiredMixin,
    DeleteView,
):
    group_required = ['gerente_geral', 'administradores']
    model = RegistroReabastecimento
    template_name = 'reabastecimento/form_delete.html'
    context_object_name = 'registro'
    success_url = reverse_lazy('servicos:abastecimento:listar_reabastecimento')

    def post(self, request, *args, **kwargs):

        obj = self.get_object()

        request.session['registro_a_deletar'] = obj.pk
        request.session['next'] = request.POST.get('next')

        return redirect(
            'servicos:abastecimento:validacao_token_deletar_reabastecimento'
        )
