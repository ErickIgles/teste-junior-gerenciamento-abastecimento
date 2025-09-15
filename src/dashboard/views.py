from django.views.generic import TemplateView
from django.db.models import Sum
from django.utils.timezone import now
from datetime import timedelta

from cadastros.tanques.models import Combustivel

from servicos.abastecimento.models import (
    RegistroAbastecimento,
    RegistroReabastecimento
)


class DashboardView(TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        filtro = self.request.GET.get("filtro", "mes")  # dia, mes, ano
        combustivel_id = self.request.GET.get("combustivel")

        hoje = now().date()
        if filtro == "dia":
            inicio = hoje
        elif filtro == "ano":
            inicio = hoje.replace(month=1, day=1)
        else:  # mês
            inicio = hoje.replace(day=1)

        # Filtrar abastecimentos e reabastecimentos
        qs_abastecimentos = RegistroAbastecimento.objects.filter(criado__gte=inicio)
        qs_reabastecimentos = RegistroReabastecimento.objects.filter(criado__gte=inicio)

        if combustivel_id:
            qs_abastecimentos = qs_abastecimentos.filter(tipo_combustivel_id=combustivel_id)
            qs_reabastecimentos = qs_reabastecimentos.filter(tanque__tipo_combustivel_id=combustivel_id)

        # Totais
        abastecimentos_total = qs_abastecimentos.aggregate(Sum("valor_total_abastecimento"))["valor_total_abastecimento__sum"] or 0
        reabastecimentos_total = qs_reabastecimentos.aggregate(Sum("valor_total_reabastecimento"))["valor_total_reabastecimento__sum"] or 0

        # Combustíveis mais vendidos
        combustiveis = (
            qs_abastecimentos.values("tipo_combustivel__nome_combustivel")
            .annotate(total=Sum("litros_abastecido"))
            .order_by("-total")
        )

        # Fornecedores mais pedidos
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
