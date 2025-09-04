from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('cadastros/', include('cadastros.urls')),
    path('servicos/', include('servicos.urls')),
    path('auth/', include('autenticacao.urls')),
    path('relatorios/', include('relatorios.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
