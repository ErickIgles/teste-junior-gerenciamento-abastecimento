from django.urls import path
from .views import (

    RegistroAbastecimentoCadastroView,
    RegitroAbastecimentoListaView,
    RegistroAbastecimentoAtualizarView,
    RegistroAbastecimentoDeletarView,
    )


app_name = 'abastecimento'
urlpatterns = [

    path(
        'cadastrar/',
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
]
