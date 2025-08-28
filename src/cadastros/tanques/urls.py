from django.urls import path

from .views import (
    TanqueCadastroView,
    TanqueListarView,
    TanqueAtualizarView,
    # TanqueDeletarView,
    # TanqueInativarView,
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
    )
    # path('deletar/<int:pk>/', TanqueDeletarView.as_view(), name='deletar'),
    # path('inativar/<int:pk>/', TanqueInativarView.as_view(), name='inativar')
]
