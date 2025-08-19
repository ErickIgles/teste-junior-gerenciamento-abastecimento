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
        'empresa',
        'criado',
        'modificado',
        'ativo'
    ]
    list_display_links = ['id', 'nome_combustivel']



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
    list_display_links = ['id', 'tipo_combustivel', 'identificador_tanque', 'capacidade_maxima', 'quantidade_disponivel']
