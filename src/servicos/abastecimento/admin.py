from django.contrib import admin


from .models import RegistroAbastecimento, RegistroReabastecimento


@admin.register(RegistroAbastecimento)
class RegistroAbastecimentoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'funcionario',
        'empresa',
        'tanque',
        'bomba',
        'tipo_combustivel',
        'litros_abastecido',
        'valor_total_abastecimento',
        'criado',
        'modificado',
        'ativo'
    ]

    list_display_links = [
        'id',
        'tanque'
    ]

    list_filter = [
        'funcionario',
        'empresa',
        'tanque',
        'bomba'
    ]

    ordering = (
        'id',
        'criado',
    )



@admin.register(RegistroReabastecimento)
class RegistroReabastecimentoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'tanque',
        'quantidade',
        'funcionario',
        'valor_total_reabastecimento',
        'empresa',
        'criado',
        'modificado',
        'ativo'
    ]

    list_display_links = [
        'id',
        'tanque',
    ]

    search_fields = [
        'tanque',
        'empresa'
    ]

    list_filter = [
        'empresa',
        'funcionario',
        'tanque'
    ]

    ordering = (
        'id',
    )
