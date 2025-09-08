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
        'empresa',
        'criado',
        'modificado',
        'ativo'
    ]

    list_display_links = [
        'id',
        'tanque',
    ]

    ordering = (
        'id',
    )
