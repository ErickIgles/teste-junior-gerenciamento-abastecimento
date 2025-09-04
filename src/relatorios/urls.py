from django.urls import path


from .views import RelatorioAbastecimento, RelatorioAbastecimentoDetalhe


app_name = 'relatorios'
urlpatterns = [
    path(
        '',
        RelatorioAbastecimento.as_view(),
        name='listar'
    ),
    path(
        'detalhes/<int:pk>/',
        RelatorioAbastecimentoDetalhe.as_view(),
        name='detalhe'
    ),
]
