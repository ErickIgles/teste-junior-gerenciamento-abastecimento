from django.urls import path, include


app_name='cadastros'

urlpatterns = [
    # path('bombas/', include('cadastros.bombas.urls')),
     path('tanques/', include('cadastros.tanques.urls')),
]