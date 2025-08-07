from django.contrib import admin

from .models import Tanque


@admin.register(Tanque)
class TanqueAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_combustivel', 'identificador_tanque', 'capacidade_maxima', 'quantidade_disponivel']
    list_display_links = ['id', 'tipo_combustivel', 'identificador_tanque', 'capacidade_maxima', 'quantidade_disponivel']
