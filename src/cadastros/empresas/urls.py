from django.urls import path

from .views import (
    EmpresaCriarView,
    EmpresaPerfilView,
    EmpresaInativarView,

    SetorCadastrarView,
    SetorListarView,
    SetorAtualizarView,
    SetorDeletarView,

    CargoCadastrarView,
    CargoListarView,
    CargoAtualizarView,
    CargoDeletarView
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
    ),

    path(
        'cargo/cadastrar/',
        CargoCadastrarView.as_view(),
        name='cadastrar_cargo'
    ),
    path(
        'cargo/listar/',
        CargoListarView.as_view(),
        name='listar_cargo'
    ),
    path(
        'cargo/atualizar/<int:pk>/',
        CargoAtualizarView.as_view(),
        name='atualizar_cargo'
    ),
    path(
        'cargo/deletar/<int:pk>/',
        CargoDeletarView.as_view(),
        name='deletar_cargo'
    )
]
