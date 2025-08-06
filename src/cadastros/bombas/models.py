from django.db import models

from core.models import Base
from ..tanques.models import Tanque


class Bomba(Base):
    nome_bomba = models.CharField(verbose_name='Nome', max_length=144)
    tanque = models.OneToOneField(Tanque, verbose_name='Tanque', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Bomba'
        verbose_name_plural = 'Bombas'
    
    def __str__(self):
        return f'{self.nome_bomba} - {self.tanque.tipo_combustivel}'

