from datetime import datetime

from django.shortcuts import get_object_or_404

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

    def get_empresa_do_objeto(self):
        reabastecimento = RegistroAbastecimento.objects.select_related("empresa").filter(
            pk=self.kwargs["pk"]
        ).first()
        return reabastecimento.empresa if reabastecimento else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        usuario = self.request.user

        if usuario.is_empresa():

            empresa = Empresa.objects.get(usuario_responsavel=usuario)

        else:
            empresa = Funcionario.objects.select_related("empresa").get(user=usuario).empresa

        abastecimento = get_object_or_404(
            RegistroAbastecimento.objects.select_related('bomba', 'funcionario'),
            id=self.kwargs['pk'],
            empresa=empresa,
        )

        context.update({
            'abastecimento': abastecimento,
            'bomba': abastecimento.bomba,
            'tanque': abastecimento.bomba.tanque,
        })

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
            'empresa', 'funcionario'
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

    def get_empresa_do_objeto(self):
        reabastecimento = RegistroReabastecimento.objects.select_related("empresa").filter(
            pk=self.kwargs["pk"]
        ).first()
        return reabastecimento.empresa if reabastecimento else None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        reabastecimento_id = self.kwargs["pk"]
        usuario = self.request.user

        if usuario.is_empresa():
            empresa = Empresa.objects.get(usuario_responsavel=usuario)
        else:
            empresa = Funcionario.objects.select_related("empresa").get(user=usuario).empresa

        reabastecimento = RegistroReabastecimento.objects.select_related(
            "fornecedor", "tanque", "funcionario", "empresa"
        ).get(pk=reabastecimento_id, empresa=empresa)

        context["reabastecimento"] = reabastecimento
        context["tanque"] = reabastecimento.tanque
        context["total_litros"] = reabastecimento.quantidade
        context["total_valor"] = reabastecimento.valor_total_reabastecimento

        return context


class RelatorioReabastecimentoDetalhadoPDF(
    RelatorioReabastecimentoDetalhado
):

    def get(self, request, *args, **kwargs):
        # pega o pk do reabastecimento
        reabastecimento_id = self.kwargs.get("pk")

        # busca apenas esse reabastecimento
        reabastecimento = RegistroReabastecimento.objects.select_related(
                'fornecedor',
                'tanque',
                'funcionario',
                'empresa'
            ).get(
                pk=reabastecimento_id
            )

        total_litros = reabastecimento.quantidade
        total_valor = reabastecimento.valor_total_reabastecimento

        # renderiza o template PDF
        html_string = render_to_string(
            'relatorios/reabastecimento/reabastecimento_detalhado_pdf.html',
            {
                'reabastecimento': reabastecimento,
                'total_litros': total_litros,
                'total_valor': total_valor,
                'data_inicio': reabastecimento.criado,
                'data_fim': reabastecimento.criado,
            }
        )

        pdf_file = generate_pdf(source=html_string)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reabastecimento_{reabastecimento_id}.pdf"'

        return response
