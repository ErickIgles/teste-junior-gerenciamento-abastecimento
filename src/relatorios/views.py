from django.views import View

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
        funcionario_id = self.request.GET.get('funcionario')
        tipo_combustivel = self.request.GET.get('tipo_combustivel')
        forma_pagamento = self.request.GET.get('forma_pagamento')

        if q:

            abastecimentos = abastecimentos.filter(
                Q(funcionario__username__icontains=q) |
                Q(
                    tanque__tipo_combustivel__nome_combustivel__icontains=q
                )
            )

        if data_inicio and data_fim:

            abastecimentos = abastecimentos.filter(
                criado__range=[data_inicio, data_fim]
            )

        if funcionario_id:

            try:
                abastecimentos = abastecimentos.filter(

                    Q(funcionario=int(funcionario_id))
                )
            except ValueError:
                        # Continua se o valor não for um número
                pass

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


class RelatorioAbastecimentoDetalhadoPDF(View):

    def _get_empresa_do_usuario(self, usuario_logado):
        """
        Método privado para buscar a empresa associada ao usuário,
        evitando múltiplas consultas.
        """
        try:
            return usuario_logado.funcionario.empresa
        except Funcionario.DoesNotExist:
            pass
        
        try:
            return Empresa.objects.select_related('usuario_responsavel').get(
                usuario_responsavel=usuario_logado
            )
        except Empresa.DoesNotExist:
            return None

    def _get_abastecimentos(self, request, empresa):
        """
        Encapsula a lógica de filtragem para a geração do PDF.
        """
        abastecimentos = RegistroAbastecimento.objects.select_related(
            'empresa', 'funcionario', 'tipo_combustivel', 'tanque'
        ).filter(
            empresa=empresa
        )
        
        q = request.GET.get('q')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        funcionario = request.GET.get('funcionario')
        tipo_combustivel_id = request.GET.get('tipo_combustivel')
        forma_pagamento = request.GET.get('forma_pagamento')

        if q:
            abastecimentos = abastecimentos.filter(
                Q(funcionario__username__icontains=q) |
                Q(tanque__tipo_combustivel__nome_combustivel__icontains=q)
            )
        
        if data_inicio and data_fim:
            abastecimentos = abastecimentos.filter(
                criado__range=[data_inicio, data_fim]
            )

        if funcionario:
            abastecimentos = abastecimentos.filter(
                funcionario=funcionario
            )

        if tipo_combustivel_id:
            abastecimentos = abastecimentos.filter(
                tipo_combustivel_id=tipo_combustivel_id
            )

        if forma_pagamento:
            abastecimentos = abastecimentos.filter(
                forma_pagamento=forma_pagamento
            )
        
        return abastecimentos.order_by('-criado')

    def get(self, request, *args, **kwargs):
        
        empresa = self._get_empresa_do_usuario(request.user)
        
        if not empresa:
        
            return HttpResponse("Acesso negado.", status=403)
        
        # Chama o método interno para obter os dados filtrados
        abastecimentos = self._get_abastecimentos(request, empresa)
        
        total_litros = abastecimentos.aggregate(
            total=Sum('litros_abastecido')
        )['total'] or 0
        total_valor = abastecimentos.aggregate(
            total=Sum('valor_total_abastecimento')
        )['total'] or 0
        
        context = {
            'registros': abastecimentos,
            'total_litros': total_litros,
            'total_valor': total_valor,
            'funcionarios': Funcionario.objects.filter(empresa=empresa),
            'tipos_combustivel': Combustivel.objects.filter(empresa=empresa),
        }

        html_string = render_to_string(
            'relatorios/abastecimento/abastecimento_detalhado_pdf.html',
            context
        )
        
        # Sua lógica de geração de PDF
        pdf_file = generate_pdf(source=html_string)

        filename = "relatorio_abastecimento_geral.pdf"
        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        
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
        tanque = self.request.GET.get('tanque')
        tipo_combustivel = self.request.GET.get('tipo_combustivel')
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

        if tanque:

            reabastecimentos = reabastecimentos.filter(
                tanque=tanque
            )

        if tipo_combustivel:

            reabastecimentos = reabastecimentos.filter(
                tanque__tipo_combustivel=tipo_combustivel
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

        context['tipos_combustivel'] = Combustivel.objects.select_related(
            'empresa'
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


class RelatorioReabastecimentoDetalhadoPDF(
    View
):

    def _get_empresa_do_usuario(self, usuario_logado):
        """
        Método privado para buscar a empresa associada ao usuário,
        evitando múltiplas consultas.
        """
        try:
            return usuario_logado.funcionario.empresa
        except Funcionario.DoesNotExist:
            pass
        
        try:
            return Empresa.objects.select_related('usuario_responsavel').get(
                usuario_responsavel=usuario_logado
            )
        except Empresa.DoesNotExist:
            return None

    def _get_reabastecimento(self, request, empresa):

        reabastecimentos = RegistroReabastecimento.objects.select_related(
            'tanque',
            'empresa',
            'fornecedor',
            'funcionario'
        )


        q = request.GET.get('q')
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        funcionario = request.GET.get('funcionario')
        tanque = request.GET.get('tanque')
        tipo_combustivel_id = request.GET.get('tipo_combustivel')
        forma_pagamento = request.GET.get('forma_pagamento')

        if q:

            reabastecimentos = reabastecimentos.filter(
                Q(furncionario__username__icontains=q) |
                Q(tanque__identificador_tanque__icontains=q)
            )

        if data_inicio and data_fim:
            reabastecimentos = reabastecimentos.filter(
                criado__range=[data_inicio, data_fim]
            )

        if funcionario:
            reabastecimentos = reabastecimentos.filter(
                funcionario=funcionario
            )
        
        if tanque:

            reabastecimentos = reabastecimentos.filter(
                tanque=tanque
            )

        if tipo_combustivel_id:
            reabastecimentos = reabastecimentos.filter(
                tipo_combustivel_id=tipo_combustivel_id
            )

        if forma_pagamento:
            reabastecimentos = reabastecimentos.filter(
                forma_pagamento=forma_pagamento
            )
        
        return reabastecimentos.order_by('-criado')



    def get(self, request, *args, **kwargs):
        # pega o pk do reabastecimento
        
        empresa = self._get_empresa_do_usuario(request.user)


        if not empresa:
        
            return HttpResponse("Acesso negado.", status=403)


        reabastecimentos = self._get_reabastecimento(request, empresa)


        total_litros = reabastecimentos.aggregate(
            total=Sum('quantidade')
        )['total'] or 0
        total_valor = reabastecimentos.aggregate(
            total=Sum('valor_total_reabastecimento')
        )['total'] or 0
        
        context = {
            'registros': reabastecimentos,
            'total_litros': total_litros,
            'total_valor': total_valor,
        }


        # renderiza o template PDF
        html_string = render_to_string(
            'relatorios/reabastecimento/reabastecimento_detalhado_pdf.html',
            context
        )

        pdf_file = generate_pdf(source=html_string)

        response = HttpResponse(pdf_file, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reabastecimento_detalhe.pdf"'

        return response
