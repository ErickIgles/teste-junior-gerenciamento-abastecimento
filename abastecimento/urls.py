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

)

urlpatterns = [
    path('', IndexTemplateView.as_view(), name='index'),
    path('criar/tanque/', CriarTanqueView.as_view(), name='criar_tanque'),
    path('listagem/tanque/', ListaTanqueView.as_view(), name='listagem_tanque'),
    path('atualizar/tanque/<int:pk>/', AtualizarTanqueView.as_view(), name='atualizar_tanque'),
    path('deletar/tanque/<int:pk>/', DeletarTanqueView.as_view(), name='deletar_tanque'),

    path('criar/bomba/', CriarBombaView.as_view(), name='criar_bomba'),
    path('listagem/bomba/', ListaBombaView.as_view(), name='listagem_bomba'),
    path('atualizar/bomba/<int:pk>/', AtualizarBombaView.as_view(), name='atualizar_bomba'),
    path('deletar/bomba/<int:pk>/', DeletarBombaView.as_view(), name='deletar_bomba'),

]