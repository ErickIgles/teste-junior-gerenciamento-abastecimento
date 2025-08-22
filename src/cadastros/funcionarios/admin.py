from django.contrib import admin

from .models import Funcionario


@admin.register(Funcionario)
class FuncionarioAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'nome_funcionario',
        'user',
        'empresa',
        'cargo',
        'criado',
        'modificado',
        'ativo'
    ]
    list_display_links = [
        'id',
        'nome_funcionario',
        'user'
    ]
    ordering = [
        'nome_funcionario',
        'user',
        'criado'
    ]
    search_fields = [
        'nome_funcionario',
        'user__username',
        'cargo__cargo',
        'grupo__grupo'
    ]
