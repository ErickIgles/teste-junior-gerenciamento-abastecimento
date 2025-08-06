from django.contrib import admin

from .models import Bomba, Abastecimento



@admin.register(Bomba)
class BombaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_bomba', 'tanque']
    list_display_links = ['id', 'nome_bomba', 'tanque']


@admin.register(Abastecimento)
class AbastecimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'bomba', 'litros_abastecidos', 'valor']
    list_display_links = ['id', 'bomba', 'litros_abastecidos', 'valor']

