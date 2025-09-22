from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.utils.timezone import now

from cadastros.tanques.models import Combustivel
from cadastros.empresas.models import Empresa
from cadastros.funcionarios.models import Funcionario

from servicos.abastecimento.models import (
    RegistroAbastecimento,
    RegistroReabastecimento
)


class DashboardView(
    LoginRequiredMixin,
    TemplateView
):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filtro = self.request.GET.get("filtro", "mes")
        combustivel_id = self.request.GET.get("combustivel")

        hoje = now().date()
        if filtro == "dia":
            inicio = hoje
        elif filtro == "ano":
            inicio = hoje.replace(month=1, day=1)
        else:  # mês
            inicio = hoje.replace(day=1)

        usuario_logado = self.request.user
        if usuario_logado.is_empresa():
            empresa = Empresa.objects.get(usuario_responsavel=usuario_logado)
        else:
            usuario_funcionario = Funcionario.objects.get(user=usuario_logado)
            empresa = usuario_funcionario.empresa

        qs_abastecimentos = RegistroAbastecimento.objects.filter(
            criado__gte=inicio,
            bomba__empresa=empresa
        )
        qs_reabastecimentos = RegistroReabastecimento.objects.filter(
            criado__gte=inicio,
            tanque__empresa=empresa
        )

        if combustivel_id:
            qs_abastecimentos = qs_abastecimentos.filter(
                tipo_combustivel_id=combustivel_id
            )
            qs_reabastecimentos = qs_reabastecimentos.filter(
                tanque__tipo_combustivel_id=combustivel_id
            )

        abastecimentos_total = qs_abastecimentos.aggregate(Sum("valor_total_abastecimento"))["valor_total_abastecimento__sum"] or 0
        reabastecimentos_total = qs_reabastecimentos.aggregate(Sum("valor_total_reabastecimento"))["valor_total_reabastecimento__sum"] or 0

        combustiveis = (
            qs_abastecimentos.values("tipo_combustivel__nome_combustivel")
            .annotate(total=Sum("litros_abastecido"))
            .order_by("-total")
        )

        fornecedores = (
            qs_reabastecimentos.values("fornecedor__nome_fantasia")
            .annotate(total=Sum("quantidade"))
            .order_by("-total")
        )

        context.update({
            "filtro": filtro,
            "combustivel_id": combustivel_id,
            "abastecimentos_total": abastecimentos_total,
            "reabastecimentos_total": reabastecimentos_total,
            "combustiveis": combustiveis,
            "fornecedores": fornecedores,
            "todos_combustiveis": Combustivel.objects.all(),
        })
        return context
