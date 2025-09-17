from django.db import models


class Base(models.Model):
    criado = models.DateTimeField(
        verbose_name='Data de Crição',
        auto_now_add=True,
        null=True, 
        blank=True
    )

    modificado = models.DateTimeField(
        verbose_name='Data de Modificação',
        auto_now=True,
        null=True,
        blank=True
    )

    ativo = models.BooleanField(
        verbose_name='Ativo',
        default=True
    )

    class Meta:
        abstract = True
