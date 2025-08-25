from django.contrib import admin


from .models import RegistroAbastecimento


@admin.register(RegistroAbastecimento)
class RegistroAbastecimentoAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'funcionario',
        'tanque',
        'tipo_combustivel',
        'litros_abastecido',
        'valor_total_abastecimento'
    ]
    list_display_links = [
        'id',
        'tanque'
    ]
