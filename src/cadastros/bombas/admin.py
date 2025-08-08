from django.contrib import admin

from .models import Bomba

@admin.register(Bomba)
class BombaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_bomba', 'tanque', 'identificador_tanque']
    list_display_links = ['id', 'nome_bomba', 'tanque']


    def identificador_tanque(self, obj):
        return obj.tanque.identificador_tanque
