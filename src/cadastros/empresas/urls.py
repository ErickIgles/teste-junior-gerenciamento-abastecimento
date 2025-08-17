from django.urls import path

from .views import (
    EmpresaCriarView,
    EmpresaAtulizarView,
    EmpresaPerfilView,
    EmpresaDeletarView
)

app_name = 'empresas'
urlpatterns = [
    path('cadastrar/', EmpresaCriarView.as_view(), name='cadastrar'),
    path('atualizar/<int:pk>/', EmpresaAtulizarView.as_view(), name='atualizar'),
    path('perfil/<int:pk>/', EmpresaPerfilView.as_view(), name='perfil'),
    path('perfil/deletar/<int:pk>/', EmpresaDeletarView.as_view(), name='deletar'),
]
