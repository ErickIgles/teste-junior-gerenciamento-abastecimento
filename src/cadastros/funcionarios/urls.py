from django.urls import path

from .views import (
    FuncionarioCadastrarView,
    FuncionarioListarView,
    FuncionarioAtualizarView,
    FuncionarioDeletarView
    )


app_name = 'funcionarios'
urlpatterns = [
    path('cadastrar/', FuncionarioCadastrarView.as_view(), name='cadastrar'),
    path('listar/', FuncionarioListarView.as_view(), name='listar'),
    path('atualizar/<int:pk>/', FuncionarioAtualizarView.as_view(), name='atualizar'),
    path('deletar/<int:pk>/', FuncionarioDeletarView.as_view(), name='deletar')
]