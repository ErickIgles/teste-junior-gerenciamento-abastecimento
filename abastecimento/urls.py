from django.urls import path
from .views import (
    IndexTemplateView,
    CriarTanqueView,
    ListaTanqueView,
    AtualizarTanqueView,
    DeletarTanqueView
)

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('criar/tanque/', CriarTanqueView.as_view(), name='criar_tanque'),
    path('listagem/tanque/', ListaTanqueView.as_view(), name='listagem_tanque'),
    path('atualizar/tanque/<int:pk>/', AtualizarTanqueView.as_view(), name='atualizar_tanque'),
    path('deletar/tanque/<int:pk>/', DeletarTanqueView.as_view(), name='deletar_tanque'),
]