from django.contrib import admin

from .models import Tanque, Combustivel



@admin.register(Combustivel)
class CombustivelAdmin(admin.ModelAdmin):    

    list_display = [
        'id',
        'nome_combustivel',
        'valor_base',
        'imposto',
        'valor_total',
        'valor_compra',
        'empresa',
        'criado',
        'modificado',
        'ativo'
    ]

    list_display_links = [
        'id',
        'nome_combustivel',
    ]

    list_filter = [
        'nome_combustivel',
        'empresa'
    ]

    search_fields = [
        'nome_combustivel',
        'empresa',
    ]

    ordering = (
        'id',
    )


@admin.register(Tanque)
class TanqueAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'tipo_combustivel',
        'identificador_tanque',
        'capacidade_maxima',
        'quantidade_disponivel',
        'empresa',
        'criado',
        'modificado',
        'ativo'
    ]

    list_filter = [
        'tipo_combustivel',
        'capacidade_maxima',
        'empresa',
    ]

    list_display_links = [
        'id',
        'tipo_combustivel',
        'identificador_tanque',
    ]

    search_fields = [
        'identificador_tanque',
        'tipo_combustivel',
    ]

    ordering = (
        'id',
    )
