from django.urls import path

from .views import (
    TanqueCadastroView,
    TanqueListarView,
    TanqueAtualizarView,
    TanqueDeletarView
)

app_name = 'tanques'

urlpatterns = [
    path('cadastrar/', TanqueCadastroView.as_view(), name='cadastrar'),
    path('listagem/', TanqueListarView.as_view(), name='listar'),
    path('atualizar/<int:pk>/', TanqueAtualizarView.as_view(), name='atualizar'),
    path('deletar/<int:pk>/', TanqueDeletarView.as_view(), name='deletar'),
]
