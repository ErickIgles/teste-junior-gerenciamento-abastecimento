from django.db import models

from django.contrib.auth.models import User

from core.models import Base


class Empresa(Base):
    nome_empresa = models.CharField(
        max_length=255,
        verbose_name="Nome da Empresa",
        unique=True
    )
    cnpj = models.CharField(
        max_length=18,
        unique=True,
        verbose_name="CNPJ"
    )
    telefone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        verbose_name="Telefone"
    )
    email = models.EmailField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Email"
    )
    usuario_responsavel = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Responsável"
    )

    def __str__(self):
        return f'{self.nome_empresa}'

    class Meta:
        verbose_name = "Empresa"
        verbose_name_plural = "Empresas"


class Setor(Base):
    nome_setor = models.CharField(
        max_length=225,
        verbose_name='Setor'
    )
    empresa = models.ForeignKey(
        Empresa,
        verbose_name='Empresa',
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'

    def __str__(self):
        return f'{self.nome_setor}'


class Cargo(Base):
    nome_cargo = models.CharField(
        max_length=255,
        verbose_name='Cargo'
    )
    setor = models.ForeignKey(
        Setor,
        verbose_name='Setor',
        on_delete=models.CASCADE
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        verbose_name='empresa',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return f'{self.nome_cargo}'


def is_empresa(user):
    return Empresa.objects.filter(usuario_responsavel=user).exists()


User.add_to_class('is_empresa', is_empresa)
