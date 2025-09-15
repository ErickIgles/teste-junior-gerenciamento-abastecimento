from django.db import models


from core.models import Base

from cadastros.empresas.models import Empresa
# Create your models here.


class Fornecedor(Base):

    razao_social = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Razão Social"
    )
    nome_fantasia = models.CharField(
        max_length=255,
        verbose_name="Nome Fantasia"
    )
    cnpj = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="CNPJ"
    )
    contato_principal = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Pessoa de Contato"
    )
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Telefone"
    )
    email = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="E-mail"
    )
    endereco = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Endereço"
    )
    observacoes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Observações"
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name='fornecedores',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome_fantasia

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
        ordering = ['nome_fantasia']
