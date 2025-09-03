from django.urls import path

from .views import (
    FuncionarioCadastrarView,
    FuncionarioListarView,
    FuncionarioAtualizarView,
)


app_name = 'funcionarios'
urlpatterns = [
    path(
        'cadastrar/',
        FuncionarioCadastrarView.as_view(),
        name='cadastrar'
    ),
    path(
        'listar/',
        FuncionarioListarView.as_view(),
        name='listar'
    ),
    path(
        'atualizar/<int:pk>/',
        FuncionarioAtualizarView.as_view(),
        name='atualizar'
    ),
]
