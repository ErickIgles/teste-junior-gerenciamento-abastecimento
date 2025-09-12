from datetime import datetime

from django.shortcuts import render, redirect

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

from weasyprint import HTML

from cadastros.empresas.models import Empresa
from cadastros.funcionarios.models import Funcionario
from cadastros.tanques.models import Combustivel, Tanque


class RelatorioAbastecimentos(
    LoginRequiredMixin,

    ListView
):

    model = RegistroAbastecimento
    template_name = 'relatorios/abastecimentos.html'

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


class RelatorioAbastecimentosPDF(RelatorioAbastecimentos):

    def get(self, request, *args, **kwargs):

        usuario = self.get_user()
        queryset = self.apply_filters(usuario=usuario)

        totais = queryset.aggregate(
            total_litros=Sum('litros_abastecido'),
            total_valor=Sum('valor_total_abastecimento')
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
            'relatorios/abastecimentos_pdf.html',
            {
                'abastecimentos': queryset,
                'total_litros': totais['total_litros'] or 0,
                'total_valor': totais['total_valor'] or 0,
                'data_inicio': data_inicio,
                'data_fim': data_fim
            }
        )

        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['content-Disposition'] = 'attachment; filename="relatorio_abastecimento.pdf"'

        return response


class RelatorioReabastecimentos(
    LoginRequiredMixin,

    ListView
):

    model = RegistroReabastecimento
    template_name = 'relatorios/reabastecimentos.html'

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


class RelatorioReabastecimentosPDF(
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
            'relatorios/reabastecimentos_pdf.html',
            {
                'reabastecimentos': queryset,
                'total_litros': totais['total_litros'] or 0,
                'total_valor': totais['total_valor'] or 0,
                'data_inicio': data_inicio,
                'data_fim': data_fim
            }
        )

        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['content-Disposition'] = 'attachment; filename="relatorio_reabastecimento.pdf"'

        return response


class RelatorioTanqueAbastecimentoDetalhado(
    LoginRequiredMixin,
    TemplateView
):
    template_name = 'relatorios/tanque_detalhado.html'

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


class RelatorioTanqueAbastecimentoDetalhadoPDF(
    RelatorioTanqueAbastecimentoDetalhado
):

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)

        html_string = render_to_string(
            'relatorios/tanque_detalhado_pdf.html', context
        )

        pdf_file = HTML(string=html_string).write_pdf()

        response = HttpResponse(pdf_file, content_type='application/pdf')

        response['Content-Disposition'] = f'attachment; filename="relatorio_tanque_{context["tanque"].id}.pdf"'

        return response
