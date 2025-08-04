from django.urls import path
from .views import (
    IndexTemplateView,
    CriarTanqueView,
    ListaTanqueView,
    AtualizarTanqueView,
    DeletarTanqueView,

    CriarBombaView,
    ListaBombaView,
    AtualizarBombaView,
    DeletarBombaView,

    CriarRegistroAbastecimentoView,
    ListaRegitroAbastecimentoView,
    AtualizarRegistroAbastecimentoView,
    DeletaRegistroAbastecimentoView,
)

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('criar/tanque/', CriarTanqueView.as_view(), name='criar_tanque'),
    path('listagem/tanque/', ListaTanqueView.as_view(), name='listagem_tanque'),
    path('listagem/atualizar/tanque/<int:pk>/', AtualizarTanqueView.as_view(), name='atualizar_tanque'),
    path('listagem/deletar/tanque/<int:pk>/', DeletarTanqueView.as_view(), name='deletar_tanque'),

    path('criar/bomba/', CriarBombaView.as_view(), name='criar_bomba'),
    path('listagem/bomba/', ListaBombaView.as_view(), name='listagem_bomba'),
    path('listagem/atualizar/bomba/<int:pk>/', AtualizarBombaView.as_view(), name='atualizar_bomba'),
    path('listagem/deletar/bomba/<int:pk>/', DeletarBombaView.as_view(), name='deletar_bomba'),

    path('criar/abastecimento/', CriarRegistroAbastecimentoView.as_view(), name='criar_abastecimento'),
    path('listagem/abastecimento/', ListaRegitroAbastecimentoView.as_view(), name='listagem_abastecimento'),
    path('listagem/atualizar/abastecimento/<int:pk>/', AtualizarRegistroAbastecimentoView.as_view(), name='atualizar_abastecimento'),
    path('listagem/deletar/abastecimento/<int:pk>/', DeletaRegistroAbastecimentoView.as_view(), name='deletar_abastecimento'),
]