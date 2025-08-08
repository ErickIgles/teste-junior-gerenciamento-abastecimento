from django.db import models

from core.models import Base

from ..tanques.models import Tanque
    

class Combustivel(Base):
    class TipoCombustivel(models.TextChoices):
    
        GASOLINA = 'GASOLINA', 'Gasolina'
        DIESEL = 'DIESEL', 'Óleo Diesel'

    nome_combustivel = models.CharField(verbose_name='Nome do Combustível', max_length=100, choices=TipoCombustivel.choices)
    valor_base = models.DecimalField(verbose_name='Preço', max_digits=10, decimal_places=2)
    imposto = models.DecimalField(verbose_name='Imposto', max_digits=10, decimal_places=2, default=0.0)
    valor_total = models.DecimalField(verbose_name='Valor Total', max_digits=10, decimal_places=2, default=0.0)


    class Meta:
        verbose_name = 'Combustível'
        verbose_name_plural = 'Combustíveis'

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_base + (self.valor_base * (self.imposto/100)) 
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome_combustivel}'


class RegistroAbastecimento(Base):
    
    tanque = models.ForeignKey(Tanque, verbose_name='Tanque', on_delete=models.CASCADE)
    tipo_combustivel = models.ForeignKey(Combustivel ,verbose_name='Tipo de combustivel', on_delete=models.PROTECT)
    litros_abastecer = models.DecimalField(verbose_name='Quantidade a abastecer', max_digits=10, decimal_places=2)
    valor_total_abastecimento = models.DecimalField(verbose_name='Valor total', max_digits=10, decimal_places=2, default=0.0)

    class Meta:
        verbose_name = 'Registro de Combustível'
        verbose_name_plural = 'Registros de Combustível'

    def save(self, *args, **kwargs):
        self.valor_total_abastecimento = self.tipo_combustivel.valor_total * self.litros_abastecer
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.tipo_combustivel} - {self.litros_abastecer}L - R$ {self.valor_total_abastecimento}'
    
