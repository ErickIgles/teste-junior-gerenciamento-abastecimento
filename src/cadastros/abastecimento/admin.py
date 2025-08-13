from django.contrib import admin

from .models import Combustivel, RegistroAbastecimento



@admin.register(Combustivel)
class CombustivelAdmin(admin.ModelAdmin):    
    list_display = ['id', 'nome_combustivel', 'valor_base', 'imposto', 'valor_total']
    list_display_links = ['id', 'nome_combustivel']


@admin.register(RegistroAbastecimento)
class RegistroAbastecimentoAdmin(admin.ModelAdmin):
    list_display = ['id', 'funcionario', 'identificador_tanque', 'tipo_combustivel', 'litros_abastecido', 'valor_total_abastecimento']
    list_display_links = ['id', 'identificador_tanque']

    def identificador_tanque(self, obj):
        return obj.tanque.identificador_tanque
    
