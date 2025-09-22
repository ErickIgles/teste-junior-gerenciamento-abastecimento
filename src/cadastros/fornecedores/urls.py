from django.urls import path
from .views import (
    FornecedorCadastroView,
    FornecedorListarView,
    FornecedorAtualizarView,
    FornecedorDeletarView
)

app_name = 'fornecedores'

urlpatterns = [
    path(
        'listar/',
        FornecedorListarView.as_view(),
        name='listar'
    ),
    path(
        'cadastrar/',
        FornecedorCadastroView.as_view(),
        name='cadastrar'
    ),
    path(
        'editar/<int:pk>',
        FornecedorAtualizarView.as_view(),
        name='atualizar'
    ),
    path(
        'deletar/<int:pk>/',
        FornecedorDeletarView.as_view(),
        name='deletar'
    )
]
