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

from .utils.validacao import (
    gerador_qr,
    pagina_qr,
    validacao_token_criar_reabastecimento,
    validacao_token_deletar_reabastecimento,
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
    ),

    path(
        'qr/',
        pagina_qr,
        name='pagina_qr'
    ),

    path(
        'qr-img/',
        gerador_qr,
        name='gerador_qr'
    ),
    path(
        'validacao/',
        validacao_token_criar_reabastecimento,
        name='validacao_token_cadastrar_reabastecimento'
    ),

    path(
        'validar-token/deletar/',
        validacao_token_deletar_reabastecimento,
        name='validacao_token_deletar_reabastecimento'
    )

]
