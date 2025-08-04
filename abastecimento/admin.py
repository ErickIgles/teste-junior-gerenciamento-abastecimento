from django.contrib import admin

from .models import Tanque, Bomba, Abastecimento


@admin.register(Tanque)
class TanqueAdmin(admin.ModelAdmin):
    list_display = ['id', 'tipo_combustivel', 'quantidade']
    list_display_links = ['id', 'tipo_combustivel', 'quantidade']


@admin.register(Bomba)
class BombaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_bomba', 'tanque']
    list_display_links = ['id', 'nome_bomba', 'tanque']


@admin.register(Abastecimento)
class AbastecimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'bomba', 'litros_abastecidos', 'valor']
    list_display_links = ['id', 'bomba', 'litros_abastecidos', 'valor']

