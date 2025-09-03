from django.contrib import admin


from .models import Empresa, Setor, Cargo


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'nome_empresa',
        'cnpj',
        'telefone',
        'email',
        'usuario_responsavel',
        'criado',
        'modificado',
        'ativo'
    ]

    list_display_links = [
        'id',
        'nome_empresa',
        'cnpj'
    ]

    ordering = (
        'id',
        'criado',
    )

    list_filter = [
        'nome_empresa',
        'cnpj',
        'email',
    ]

    search_fields = ('nome_empresa',)


@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'nome_setor',
        'empresa',
        'criado',
        'modificado',
        'ativo'
    ]

    list_display_link = [
        'id',
        'nome_setor'
    ]

    ordering = (
        'id',
        'criado',
    )

    list_filter = [
        'nome_setor',
        'empresa'
    ]

    search_fields = ('nome_setor',)


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'nome_cargo',
        'setor',
        'empresa',
        'criado',
        'modificado',
        'ativo'
    ]

    list_display_link = [
        'id',
        'nome_cargo'
    ]

    ordering = (
        'id',
        'criado',
    )

    list_filter = [
        'nome_cargo',
        'setor',
        'empresa'
    ]

    search_fields = ('nome_cargo',)
