from django.db import models

from django.contrib.auth.models import User, Group

from core.models import Base
from cadastros.empresas.models import Cargo



class Funcionario(Base):
    nome_funcionario = models.CharField(verbose_name='Nome do Funcionário', max_length=100, default='')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name='Cargo')

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
    
    def __str__(self):
        return f'{self.nome_funcionario}'
    
