from django.urls import path
from .views import (
    FuncionarioLoginView,
    EmpresaLoginFormView,
    UsuarioLogoutView,

)
app_name = 'autenticacao'

urlpatterns = [
    path(
        'login/funcionário/',
        FuncionarioLoginView.as_view(),
        name='login'
    ),

    path(
        'logout/',
        UsuarioLogoutView.as_view(),
        name='logout'
    ),

    path(
        'login/empresa/',
        EmpresaLoginFormView.as_view(),
        name='login_empresa'
    ),
]
