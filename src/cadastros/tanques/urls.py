from django.urls import path

from .views import (
    TanqueCadastroView,
    TanqueListarView,
    TanqueAtualizarView,

    CombustivelCadastroView,
    CombustivelListarView,
    CombustivelAtualizarView,
    CombustivelDeletarView
)

app_name = 'tanques'

urlpatterns = [
    path(
        'cadastrar/',
        TanqueCadastroView.as_view(),
        name='cadastrar'
    ),
    path(
        'listar/',
        TanqueListarView.as_view(),
        name='listar'
    ),
    path(
        'atualizar/<int:pk>/',
        TanqueAtualizarView.as_view(),
        name='atualizar'
    ),

    path(
        'combustiveis/cadastrar/',
        CombustivelCadastroView.as_view(),
        name='cadastrar_combustivel',
    ),
    path(
        'combustiveis/listar/',
        CombustivelListarView.as_view(),
        name='listar_combustivel'
    ),
    path(
        'combustivel/atualizar/<int:pk>/',
        CombustivelAtualizarView.as_view(),
        name='atualizar_combustivel',
    ),
    path(
        'combustivel/deletar/<int:pk>/',
        CombustivelDeletarView.as_view(),
        name='deletar_combustivel'
    )

]
