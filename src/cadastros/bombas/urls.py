from django.urls import path

from .views import (
    BombaAtualizarView,
    BombaCadastroView,
    BombaInativarView,
    BombaListarView
)

app_name = 'bombas'

urlpatterns = [
    path(
        'cadastrar/',
        BombaCadastroView.as_view(),
        name='cadastrar'
        ),
    path(
        'listar/',
        BombaListarView.as_view(),
        name='listar'
        ),
    path(
        'atualizar/<int:pk>/',
        BombaAtualizarView.as_view(),
        name='atualizar'
        ),
    path(
        'inativar/<int:pk>/',
        BombaInativarView.as_view(),
        name='inativar'
        ),
]
