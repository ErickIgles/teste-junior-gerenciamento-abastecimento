from django.contrib import admin

from .models import Setor, Cargo, Funcionario


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ['id', 'setor', 'criado', 'modificado', 'ativo']
    list_display_links = ['id', 'setor']
    ordering = ['setor', 'criado']


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ['id', 'cargo', 'criado', 'modificado', 'ativo']
    list_display_links = ['id', 'cargo']
    ordering = ['cargo', 'criado']


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cargo', 'grupo', 'setor', 'criado', 'modificado', 'ativo']
    list_display_links = ['id', 'user']
    ordering = ['user', 'criado']
    search_fields = ['user__username', 'cargo__cargo', 'grupo__grupo' ,'setor__setor']
