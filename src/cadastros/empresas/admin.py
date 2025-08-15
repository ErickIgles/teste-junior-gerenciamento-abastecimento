from django.contrib import admin


from .models import Empresa


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome_empresa', 'cnpj', 'telefone', 'email', 'usuario_responsavel', 'criado', 'modificado', 'ativo']
    list_display_links = ['id', 'nome_empresa', 'cnpj']
    ordering = ('id', )
    search_fields = ('nome_empresa',)
