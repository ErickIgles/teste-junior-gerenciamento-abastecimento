from django.urls import path

from .views import (
    EmpresaCriarView,
    EmpresaPerfilView,
    # EmpresaDeletarView
    EmpresaInativarView,
)

app_name = 'empresas'
urlpatterns = [
    path(
        'cadastrar/',
        EmpresaCriarView.as_view(),
        name='cadastrar'
    ),
    path(
        'perfil/',
        EmpresaPerfilView.as_view(),
        name='perfil'
    ),
    path(
        'perfil/deletar/<int:pk>/',
        EmpresaInativarView.as_view(),
        name='inativar'
    ),
]
