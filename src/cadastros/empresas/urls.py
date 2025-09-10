from django.urls import path

from .views import (
    EmpresaCriarView,
    EmpresaPerfilView,
    EmpresaInativarView,

    SetorCadastrarView,
    SetorListarView,
    SetorAtualizarView,
    SetorDeletarView,
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

    path(
        "setro/cadastrar/",
        SetorCadastrarView.as_view(),
        name="cadastrar_setor"
    ),

    path(
        'setor/listar/',
        SetorListarView.as_view(),
        name='listar_setor'
    ),
    path(
        'setor/atualizar/<int:pk>/',
        SetorAtualizarView.as_view(),
        name='atualizar_setor'
    ),
    path(
        'setor/deletar/<int:pk>/',
        SetorDeletarView.as_view(),
        name='deletar_setor'
    )

]
