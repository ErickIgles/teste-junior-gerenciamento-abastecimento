from datetime import datetime


from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string

from django.views.generic import ListView
from django.db.models import Q, Sum
from django.views.generic import TemplateView

from servicos.abastecimento.models import (
    RegistroAbastecimento,
    RegistroReabastecimento,
)

from pydf import generate_pdf

from cadastros.empresas.models import Empresa
from cadastros.funcionarios.models import Funcionario
from cadastros.tanques.models import Combustivel, Tanque
from .utils.mixins import EmpresaRelatorioPermissionMixin
from core.mixins import GroupRequiredMixin


class RelatorioAbastecimentos(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']
    model = RegistroAbastecimento
    template_name = 'relatorios/abastecimento/abastecimentos.html'

    def get_user(self):

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            empresa = Empresa.objects.select_related(
                'usuario_responsavel'
            ).get(
                usuario_responsavel=usuario_logado
            )

            return empresa

        funcionario = Funcionario.objects.select_related(
            'user'
        ).get(
            user=usuario_logado
        )

        empresa = Empresa.objects.select_related(
            'usuario_responsavel'
        ).get(
            usuario_responsavel=funcionario.empresa.usuario_responsavel
        )

        return empresa

    def apply_filters(self, usuario):

        abastecimentos = RegistroAbastecimento.objects.select_related(
            'empresa', 'funcionario', 'tipo_combustivel', 'tanque'
        ).filter(
            empresa=usuario
        )

        q = self.request.GET.get('q')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        funcionario = self.request.GET.get('funcionario')
        tipo_combustivel = self.request.GET.get('tipo_combustivel')
        forma_pagamento = self.request.GET.get('forma_pagamento')

        if q:

            abastecimentos = abastecimentos.filter(
                Q(funcionario__nome_funcionario__icontains=q) |
                Q(
                    tanque__tipo_combustivel__nome_combustivel__icontains=q
                )
            )

        if data_inicio and data_fim:

            abastecimentos = abastecimentos.filter(
                criado__range=[data_inicio, data_fim]
            )

        if funcionario:

            abastecimentos = abastecimentos.filter(
                funcionario=funcionario
            )

        if tipo_combustivel:

            abastecimentos = abastecimentos.filter(
                tipo_combustivel=tipo_combustivel
            )

        if forma_pagamento:

            abastecimentos = abastecimentos.filter(
                forma_pagamento=forma_pagamento
            )

        abastecimentos = abastecimentos.order_by('-criado')

        return abastecimentos

    def get_queryset(self):

        usuario = self.get_user()

        queryset = self.apply_filters(usuario=usuario)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['registros'] = self.get_queryset()

        context['tipos_combustivel'] = Combustivel.objects.select_related(
            'empresa'
        ).filter(
            empresa=self.get_user()
        )

        context['funcionarios'] = Funcionario.objects.select_related(
            'empresa', 'user'
        ).filter(
            empresa=self.get_user()
        )

        qs = context['registros']

        context['total_litros'] = qs.aggregate(
            total=Sum('litros_abastecido')
        )['total'] or 0

        context['total_valor'] = qs.aggregate(
            total=Sum('valor_total_abastecimento')
        )['total'] or 0

        return context


class RelatorioAbastecimentoDetalhado(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaRelatorioPermissionMixin,
    TemplateView
):
    group_required = ['gerente_geral', 'administradores']

    template_name = 'relatorios/abastecimento/abastecimento_detalhado.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        tanque_id = self.kwargs['pk']

        usuario = self.request.user

        if usuario.is_empresa():

            empresa = Empresa.objects.get(usuario_responsavel=usuario)

        else:

            empresa = Funcionario.objects.get(user=usuario).empresa

        data_inicio = self.request.GET.get('data_inicio')

        data_fim = self.request.GET.get('data_fim')

        abastecimentos = RegistroAbastecimento.objects.filter(
            tanque_id=tanque_id,

            empresa=empresa
        ).select_related(
            'bomba',
            'funcionario'
        )

        if data_inicio and data_fim:

            abastecimentos = abastecimentos.filter(

                criado__range=[data_inicio, data_fim]
            )

        bombas = {}
        for abastecimento in abastecimentos:

            bombas.setdefault(abastecimento.bomba, []).append(abastecimento)

        context['tanque'] = Tanque.objects.get(pk=tanque_id)

        context['bombas'] = bombas

        context['total_litros'] = abastecimentos.aggregate(
            Sum(
                'litros_abastecido'
            )
        )['litros_abastecido__sum'] or 0

        context['total_valor'] = abastecimentos.aggregate(

            Sum(
                'valor_total_abastecimento'
            )
        )['valor_total_abastecimento__sum'] or 0

        return context


class RelatorioAbastecimentoDetalhadoPDF(
    RelatorioAbastecimentoDetalhado
):

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)

        html_string = render_to_string(
            'relatorios/abastecimento/abastecimento_detalhado_pdf.html',
            context
        )

        pdf_file = generate_pdf(source=html_string)

        response = HttpResponse(pdf_file, content_type='application/pdf')

        response['Content-Disposition'] = f'attachment;filename="relatorio_tanque_{context["tanque"].id}.pdf"'

        return response


class RelatorioReabastecimentos(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):

    group_required = ['gerente_geral', 'administradores']
    model = RegistroReabastecimento
    template_name = 'relatorios/reabastecimento/reabastecimentos.html'

    def get_user(self):

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            empresa = Empresa.objects.select_related(
                'usuario_responsavel'
            ).get(
                usuario_responsavel=usuario_logado
            )

            return empresa

        funcionario = Funcionario.objects.select_related(
            'user'
        ).get(
            user=usuario_logado
        )

        empresa = Empresa.objects.select_related(
            'usuario_responsavel'
        ).get(
            usuario_responsavel=funcionario.empresa.usuario_responsavel
        )

        return empresa

    def apply_filters(self, usuario):

        reabastecimentos = RegistroReabastecimento.objects.select_related(
            'empresa', 'funcionario', 'tanque'
        ).filter(
            empresa=usuario
        )

        q = self.request.GET.get('q')
        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')
        funcionario = self.request.GET.get('funcionario')
        forma_pagamento = self.request.GET.get('forma_pagamento')

        if q:

            reabastecimentos = reabastecimentos.filter(
                Q(funcionario__nome_funcionario__icontains=q) |
                Q(
                    tanque__tipo_combustivel__nome_combustivel__icontains=q
                )
            )

        if data_inicio and data_fim:

            reabastecimentos = reabastecimentos.filter(
                criado__range=[data_inicio, data_fim]
            )

        if funcionario:

            reabastecimentos = reabastecimentos.filter(
                funcionario=funcionario
            )

        if forma_pagamento:

            reabastecimentos = reabastecimentos.filter(
                forma_pagamento=forma_pagamento
            )

            messages.info(
                self.request,
                'Não há registros de saída de combustível.'
            )

        reabastecimentos = reabastecimentos.order_by('-criado')

        return reabastecimentos

    def get_queryset(self):

        usuario = self.get_user()

        queryset = self.apply_filters(usuario=usuario)

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context['registros'] = self.get_queryset()

        context['tanques'] = Tanque.objects.select_related(
            'empresa'
        ).filter(
            empresa=self.get_user()
        )

        context['funcionarios'] = Funcionario.objects.select_related(
            'empresa', 'user'
        ).filter(
            empresa=self.get_user()
        )

        qs = context['registros']

        context['total_litros'] = qs.aggregate(
            total=Sum('quantidade')
        )['total'] or 0

        context['total_valor'] = qs.aggregate(
            total=Sum('valor_total_reabastecimento')
        )['total'] or 0

        return context


class RelatorioReabastecimentoDetalhado(
    LoginRequiredMixin,
    GroupRequiredMixin,
    EmpresaRelatorioPermissionMixin,
    TemplateView
):
    group_required = ['gerente_geral', 'administradores']
    template_name = 'relatorios/reabastecimento/reabastecimento_detalhado.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        tanque_id = self.kwargs['pk']

        usuario = self.request.user

        if usuario.is_empresa():

            empresa = Empresa.objects.select_related(
                'usuario_responsavel'
            ).get(usuario_responsavel=usuario)

        else:
            empresa = Funcionario.objects.select_related(
                'user', 'empresa'
            ).get(user=usuario).empresa

        data_inicio = self.request.GET.get('data_inicio')
        data_fim = self.request.GET.get('data_fim')

        reabastecimentos = RegistroReabastecimento.objects.select_related(
            'fornecedor', 'tanque', 'funcionario', 'empresa'
        ).filter(
            tanque_id=tanque_id,
            empresa=empresa
        )

        if data_inicio and data_fim:

            reabastecimentos = reabastecimentos.filter(
                criado__range=[data_inicio, data_fim]
            )

        fornecedores = {}
        for reabastecimento in reabastecimentos:

            fornecedores.setdefault(
                reabastecimento.fornecedor, []
            ).append(reabastecimento)

        context['tanque'] = Tanque.objects.get(pk=tanque_id)

        context['fornecedores'] = fornecedores

        context['total_litros'] = reabastecimentos.aggregate(
            Sum('quantidade')
        )['quantidade__sum'] or 0

        context['total_valor'] = reabastecimentos.aggregate(
            Sum('valor_total_reabastecimento')
        )['valor_total_reabastecimento__sum'] or 0

        return context


class RelatorioReabastecimentoDetalhadoPDF(
    RelatorioReabastecimentos
):

    def get(self, request, *args, **kwargs):

        usuario = self.get_user()
        queryset = self.apply_filters(usuario=usuario)

        totais = queryset.aggregate(
            total_litros=Sum('quantidade'),
            total_valor=Sum('valor_total_reabastecimento')
        )

        data_inicio_str = request.GET.get('data_inicio')
        data_fim_str = request.GET.get('data_fim')

        if data_inicio_str:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
        else:
            data_inicio = None

        if data_fim_str:
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()

        else:
            data_fim = None

        html_string = render_to_string(
            'relatorios/reabastecimento/reabastecimentos_detalhado_pdf.html',
            {
                'reabastecimentos': queryset,
                'total_litros': totais['total_litros'] or 0,
                'total_valor': totais['total_valor'] or 0,
                'data_inicio': data_inicio,
                'data_fim': data_fim
            }
        )

        pdf_file = generate_pdf(source=html_string)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['content-Disposition'] = 'attachment;filename="relatorio_reabastecimento.pdf"'

        return response
