from django.db import models

from simple_history.models import HistoricalRecords


class Base(models.Model):

    criado = models.DateTimeField(
        verbose_name='Data de Criação',
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

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
        ordering=['-id']
