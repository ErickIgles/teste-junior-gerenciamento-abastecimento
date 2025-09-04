from django.urls import path, include

app_name = 'servicos'

urlpatterns = [
    path(
        'abastecimento/', include('servicos.abastecimento.urls')
    )
]
