from django.urls import path

from .views import FuncionarioCadastrarView


app_name = 'funcionarios'
urlpatterns = [
    path('cadastrar/', FuncionarioCadastrarView.as_view(), name='cadastrar'),
]