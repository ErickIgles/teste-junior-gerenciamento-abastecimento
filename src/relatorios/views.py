from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


from core.mixins import GroupRequiredMixin
from cadastros.funcionarios.models import Funcionario
from cadastros.tanques.models import Tanque
from cadastros.abastecimento.models import RegistroAbastecimento
from cadastros.empresas.models import Empresa


class RelatorioAbastecimento(
    LoginRequiredMixin,
    GroupRequiredMixin,
    ListView
):
    group_required = ['gerente_geral', 'administradores']
    template_name = 'abastecimentos/relatorio.html'
    model = RegistroAbastecimento

    def get_context_data(self, **kwargs):

        usuario_logado = self.request.user

        if usuario_logado.is_empresa():

            empresa = Empresa.objects.get(
                usuario_responsavel=usuario_logado
            )

        else:

            funcionario = Funcionario.objects.get(
                user=usuario_logado
            )

            empresa = Empresa.objects.get(
                usuario_responsavel=funcionario.empresa.usuario_responsavel
            )

        context = super().get_context_data(**kwargs)
        tanques = Tanque.objects.filter(
            empresa=empresa
        )

        tanques_com_registro = []

        for tanque in tanques:

            if RegistroAbastecimento.objects.filter(tanque=tanque).exists():
                tanques_com_registro.append(tanque)

        context['tanques_com_registro'] = tanques_com_registro
        return context


class RelatorioAbastecimentoDetalhe(
    LoginRequiredMixin,
    GroupRequiredMixin,
    DetailView
):
    group_required = ['gerente_geral', 'administradores']
    template_name = 'abastecimentos/detalhe.html'
    model = Tanque
    context_object_name = 'tanque'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tanque = self.get_object()
        registros_tanque = RegistroAbastecimento.objects.filter(tanque=tanque).order_by('criado')

        soma_valores = 0

        for registro in registros_tanque:
            soma_valores += registro.valor_total_abastecimento


        context.update({
            'registros_tanque': registros_tanque,  # Todos os registros do tanque
            'soma_valores': soma_valores,  # A soma total dos valores de abastecimento
        })

        return context
