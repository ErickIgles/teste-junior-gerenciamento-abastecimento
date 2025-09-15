from django.contrib import admin


from .models import Fornecedor


@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):

    list_display = [
        'nome_fantasia',
        'cnpj',
        'contato_principal',
        'telefone',
        'email',
        'empresa'
    ]

    list_display_links = [
        'nome_fantasia',
        'cnpj',
    ]

    list_filter = [
        'razao_social',
        'nome_fantasia',
    ]

    ordering = (
        'nome_fantasia',
    )

    search_fields = (
        'nome_fantasia',
        'razao_social',
        'cnpj',
    )

    list_per_page = 20
