from django.urls import path

from .views import (
    RelatorioAbastecimentos,
    RelatorioAbastecimentoDetalhado,
    RelatorioAbastecimentoDetalhadoPDF,

    RelatorioReabastecimentos,
    RelatorioReabastecimentoDetalhado,
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
        'abastecimento/detalhado/<int:pk>/',
        RelatorioAbastecimentoDetalhado.as_view(),
        name='relatorio_abstecimento_detalhes'
    ),

    path(
        'relatorios/abastecimentos/pdf/<int:pk>/',
        RelatorioAbastecimentoDetalhadoPDF.as_view(),
        name='relatorio_abastecimento_detalhes_pdf'
    ),

    path(
        'reabastecimentos/',
        RelatorioReabastecimentos.as_view(),
        name='relatorios_reabastecimentos'
    ),

    path(
        'relatorios/reabastecimentos/<int:pk>/',
        RelatorioReabastecimentoDetalhado.as_view(),
        name='relatorio_reabastecimento_detalhes'
    ),


    path(
        'relatorios/reabastecimentos/pdf/<int:pk>/',
        RelatorioReabastecimentoDetalhadoPDF.as_view(),
        name='relatorio_reabastecimento_detalhes_pdf'
    ),
]
