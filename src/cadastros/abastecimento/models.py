from django.db import models
from core.models import Base
from django.contrib.auth.models import User

from ..tanques.models import Tanque, Combustivel


class RegistroAbastecimento(Base):
    funcionario = models.ForeignKey(
        User,
        verbose_name='Funcionário',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    tanque = models.ForeignKey(
        Tanque,
        verbose_name='Tanque',
        on_delete=models.CASCADE
    )
    tipo_combustivel = models.ForeignKey(
        Combustivel,
        verbose_name='Tipo de combustivel',
        on_delete=models.PROTECT
    )
    litros_abastecido = models.DecimalField(
        verbose_name='Quantidade a abastecida',
        max_digits=10,
        decimal_places=2
    )
    valor_total_abastecimento = models.DecimalField(
        verbose_name='Valor total',
        max_digits=10,
        decimal_places=2,
        default=0.0
    )

    class Meta:
        verbose_name = 'Registro de Combustível'
        verbose_name_plural = 'Registros de Combustível'

    def save(self, *args, **kwargs):
        self.valor_total_abastecimento = self.tipo_combustivel.valor_total * self.litros_abastecido

        if self.tanque.quantidade_disponivel < self.litros_abastecido:
            raise ValueError(
                """Quantidade insuficiente no tanque para o abastecimento."""
            )

        self.tanque.quantidade_disponivel = self.tanque.quantidade_disponivel - self.litros_abastecido

        self.tanque.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.tipo_combustivel} - {self.litros_abastecido}L - R$ {self.valor_total_abastecimento}'
