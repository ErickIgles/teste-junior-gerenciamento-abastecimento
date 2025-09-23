from django.db import models

from django.core.validators import RegexValidator
from django.contrib.auth.models import User

from core.models import Base


class Empresa(Base):
    
    razao_social = models.CharField(
        max_length=255,
        verbose_name='Razão Social',
        unique=True,
        null=True,
        blank=True
    )
    nome_fantasia = models.CharField(
        max_length=255,
        verbose_name='Nome Fantasia',
        null=True,
        blank=True
    )
    cnpj = models.CharField(
        max_length=14,
        unique=True,
        verbose_name="CNPJ",
        validators=[RegexValidator(
            r'^\d{14}$',
            'CNPJ deve conter exatamente 14 dígitos numéricos.'
        )]
    )
    telefone = models.CharField(
        max_length=11,
        blank=True,
        null=True,
        verbose_name="Telefone",
        validators=[RegexValidator(
            r'^\d{10,11}$',
            'Telefone deve conter 10 ou 11 dígitos numéricos.'
        )]
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
        return self.nome_fantasia or self.razao_social

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
