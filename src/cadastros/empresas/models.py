from django.db import models

from django.contrib.auth.models import User, Group

from core.models import Base



class Empresa(Base):
    nome_empresa = models.CharField(max_length=255, verbose_name="Nome da Empresa", unique=True)
    cnpj = models.CharField(max_length=18, unique=True, verbose_name="CNPJ")
    telefone = models.CharField(max_length=15, blank=True, null=True, verbose_name="Telefone")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Email")    
    usuario_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Responsável")

    def __str__(self):
        return f'{self.nome_empresa}'

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"



def is_empresa(user):
    return Empresa.objects.filter(usuario_responsavel=user).exists()
User.add_to_class('is_empresa', is_empresa)
