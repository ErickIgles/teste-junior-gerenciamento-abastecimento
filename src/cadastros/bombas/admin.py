from django.contrib import admin

from .models import Bomba

@admin.register(Bomba)
class BombaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_bomba', 'tanque', 'empresa']
    list_display_links = ['id', 'nome_bomba', 'tanque']
    search_fields = ('nome_bomba',)
    ordering = ('id',)


    def identificador_tanque(self, obj):
        return obj.tanque.identificador_tanque
