from django.urls import path

from .views import (
    RelatorioAbastecimentos,
    RelatorioAbastecimentoDetalhadoPDF,

    RelatorioReabastecimentos,
    RelatorioReabastecimentoDetalhadoPDF,
    
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
        RelatorioAbastecimentoDetalhadoPDF.as_view(),
        name='relatorio_abastecimento_detalhes_pdf'
    ),

    path(
        'reabastecimentos/',
        RelatorioReabastecimentos.as_view(),
        name='relatorios_reabastecimentos'
    ),

    path(
        'relatorios/reabastecimentos/pdf/',
        RelatorioReabastecimentoDetalhadoPDF.as_view(),
        name='relatorio_reabastecimento_detalhes_pdf'
    ),
]
