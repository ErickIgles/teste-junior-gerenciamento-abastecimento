from django.urls import path


from .views import UsuarioLoginView, UsuarioLogoutView

app_name = 'autenticacao'

urlpatterns = [
    path('login/', UsuarioLoginView.as_view(), name='login'),
    path('logout/', UsuarioLogoutView.as_view(), name='logout'),
]