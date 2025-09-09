from django.urls import path

from .views import (

    RegistroAbastecimentoCadastroView,
    RegitroAbastecimentoListaView,
    RegistroAbastecimentoAtualizarView,
    RegistroAbastecimentoDeletarView,

    RegistroReabastecimentoCadastrarView,
    RegistroReabastecimentoListarView,
    RegistroReabastecimentoDeletarView,
    )


app_name = 'abastecimento'
urlpatterns = [

    path(
        'saida/',
        RegistroAbastecimentoCadastroView.as_view(),
        name='cadastrar'
    ),
    path(
        'listar/',
        RegitroAbastecimentoListaView.as_view(),
        name='listar'
    ),
    path(
        'atualizar/<int:pk>/',
        RegistroAbastecimentoAtualizarView.as_view(),
        name='atualizar'
    ),
    path(
        'deletar/<int:pk>/',
        RegistroAbastecimentoDeletarView.as_view(),
        name='deletar'
    ),
    path(
        'entrada/',
        RegistroReabastecimentoCadastrarView.as_view(),
        name='cadastrar_reabastecimento'
    ),
    path(
        'entrada/listar/',
        RegistroReabastecimentoListarView.as_view(),
        name='listar_reabastecimento'
    ),
    path(
        'entrada/deletar/<int:pk>/',
        RegistroReabastecimentoDeletarView.as_view(),
        name='deletar_reabastecimento'
    )
]
