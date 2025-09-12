from django.urls import path

from .views import (
    RelatorioAbastecimentos,
    RelatorioAbastecimentosPDF,

    RelatorioReabastecimentos,
    RelatorioReabastecimentosPDF
)

app_name = 'relatorios'

urlpatterns = [

    path(
        'abastecimentos/',
        RelatorioAbastecimentos.as_view(),
        name='relatorios_abastecimentos'
    ),

    path(
        'relatorios/abastecimentos/pdf/',
        RelatorioAbastecimentosPDF.as_view(),
        name="relatorios_abastecimentos_pdf"
    ),

    path(
        'reabastecimentos/',
        RelatorioReabastecimentos.as_view(),
        name='relatorios_reabastecimentos'
    ),

    path(
        'relatorios/reabastecimentos/pdf/',
        RelatorioReabastecimentosPDF.as_view(),
        name='relatorios_reabastecimentos_pdf'
    )

]
