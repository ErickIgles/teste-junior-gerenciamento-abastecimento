from django.db import models

from core.models import Base
from ..tanques.models import Tanque
from cadastros.empresas.models import Empresa


class Bomba(Base):
    nome_bomba = models.CharField(verbose_name='Nome', max_length=144)
    tanque = models.ForeignKey(Tanque, verbose_name='Tanque', on_delete=models.SET_NULL, null=True, blank=True)
    empresa = models.ForeignKey(Empresa, verbose_name='Empresa', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Bomba'
        verbose_name_plural = 'Bombas'
    
    def __str__(self):
        return f'{self.nome_bomba} - {self.empresa}'

