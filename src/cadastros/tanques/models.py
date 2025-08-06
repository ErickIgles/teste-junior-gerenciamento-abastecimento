from django.db import models


from core.models import Base




class Tanque(Base):
    TIPO_COMBUSTIVEL_CHOICES = [
        ('GASOLINA', 'Gasolina'),
        ('DIESEL', 'Óleo Diesel')
    ]

    tipo_combustivel = models.CharField(verbose_name='Tipo de Combustivel', max_length=10, choices=TIPO_COMBUSTIVEL_CHOICES)
    capacidade_maxima = models.DecimalField(verbose_name='Capacidade Máxima', max_digits=10, decimal_places=2)
    quantidade_disponivel = models.DecimalField(verbose_name='Quantidade disponivel', max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        verbose_name = 'Tanque'
        verbose_name_plural = 'Tanques'
    
    def __str__(self):
        return f'Tanque de {self.tipo_combustivel} cadastrado.'

