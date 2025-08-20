from django.db import models


from core.models import Base
from ..empresas.models import Empresa





class Combustivel(Base):
    class TipoCombustivel(models.TextChoices):
    
        GASOLINA = 'GASOLINA', 'Gasolina'
        DIESEL = 'DIESEL', 'Óleo Diesel'

    nome_combustivel = models.CharField(
        verbose_name='Nome do Combustível', 
        max_length=100, 
        choices=TipoCombustivel.choices
    )
    valor_base = models.DecimalField(
        verbose_name='Preço', 
        max_digits=10, 
        decimal_places=2
    )
    imposto = models.DecimalField(
        verbose_name='Imposto', 
        max_digits=10, 
        decimal_places=2, 
        default=0.0
    )
    valor_total = models.DecimalField(
        verbose_name='Valor Total', 
        max_digits=10, 
        decimal_places=2, 
        default=0.0
    )
    empresa = models.ForeignKey(
        Empresa, 
        verbose_name='Empresa', 
        on_delete=models.CASCADE
    )


    class Meta:
        verbose_name = 'Combustível'
        verbose_name_plural = 'Combustíveis'

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_base + (self.valor_base * (self.imposto/100)) 
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.nome_combustivel}'



class Tanque(Base):
    tipo_combustivel = models.ForeignKey(
        Combustivel, 
        verbose_name='Tipo de Combustivel', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    identificador_tanque = models.CharField(
        verbose_name='Identificador', 
        max_length=24, 
        unique=True
    )
    capacidade_maxima = models.DecimalField(
        verbose_name='Capacidade Máxima', 
        max_digits=10, 
        decimal_places=2
    )
    quantidade_disponivel = models.DecimalField(
        verbose_name='Quantidade disponivel', 
        max_digits=10, 
        decimal_places=2, 
        default=0.00
    )
    empresa = models.ForeignKey(
        Empresa, 
        verbose_name='Empresa', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True
    )

    class Meta:
        verbose_name = 'Tanque'
        verbose_name_plural = 'Tanques'
    
    def __str__(self):
        return f'{self.identificador_tanque}'

