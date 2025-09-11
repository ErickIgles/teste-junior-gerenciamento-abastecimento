from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from core.models import Base
from cadastros.tanques.models import Tanque, Combustivel
from cadastros.bombas.models import Bomba
from cadastros.empresas.models import Empresa
from cadastros.funcionarios.models import Funcionario


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
    bomba = models.ForeignKey(
        Bomba,
        on_delete=models.PROTECT,
        verbose_name='Bomba',
        null=True,
        blank=True
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        verbose_name='Empresa',
        null=True,
        blank=True
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

        if not self.bomba:
            raise ValidationError(
                """Selecione uma bomba para o abastecimento."""
            )
        self.tanque = self.bomba.tanque

        if self.tanque.quantidade_disponivel < self.litros_abastecido:
            raise ValidationError(
                "Quantidade insuficiente no tanque para o abastecimento."
            )
        self.valor_total_abastecimento = (
            self.tanque.tipo_combustivel.valor_total * self.litros_abastecido
        )
        self.tanque.quantidade_disponivel -= self.litros_abastecido
        self.tanque.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.tipo_combustivel} - {self.litros_abastecido}L - R$ {self.valor_total_abastecimento}'


class RegistroReabastecimento(Base):

    tanque = models.ForeignKey(
        Tanque,
        on_delete=models.CASCADE,
        verbose_name='Tanque'
    )

    quantidade = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Volume'
    )

    valor_total_reabastecimento = models.DecimalField(
        verbose_name='Valor total do reabastecimento',
        max_digits=10,
        decimal_places=2,
        default=0.0
    )

    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        verbose_name='Empresa'
    )

    funcionario = models.ForeignKey(
        Funcionario,
        on_delete=models.SET_NULL,
        verbose_name='Funcionário',
        null=True,
        blank=True
    )

    class Meta:

        verbose_name = 'Reabastecimento'
        verbose_name_plural = 'Reabastecimentos'

    def save(self, *args, **kwargs):
        if (self.tanque.quantidade_disponivel + self.quantidade) > self.tanque.capacidade_maxima:

            raise ValidationError(
                'Não pode exceder a capacidade máxima do tanque.'
            )

        self.valor_total_reabastecimento = (
            self.tanque.tipo_combustivel.valor_compra * self.quantidade
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return f'{self.tanque} - {self.quantidade}'

    def aplicar_reabastecimento(self):

        tanque = self.tanque

        if (tanque.quantidade_disponivel + self.quantidade) > tanque.capacidade_maxima:
            raise ValueError(
                'Não pode exceder a capacidade máxima do tanque.'
            )

        tanque.quantidade_disponivel += self.quantidade
        tanque.save()
