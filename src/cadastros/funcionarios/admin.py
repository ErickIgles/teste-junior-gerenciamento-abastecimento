from django.contrib import admin

from .models import Funcionario



@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cargo', 'empresa' ,'criado', 'modificado', 'ativo']
    list_display_links = ['id', 'user']
    ordering = ['user', 'criado']
    search_fields = ['user__username', 'cargo__cargo', 'grupo__grupo']


    def empresa(self, obj):
        return obj.cargo.setor.empresa
    