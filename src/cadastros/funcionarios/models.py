from django.db import models

from django.contrib.auth.models import User

from core.models import Base


class Setor(Base):
    setor = models.CharField(max_length=100, verbose_name='Setor')

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'

    def __str__(self):
        return f'{self.setor}'


class Cargo(Base):
    cargo = models.CharField(max_length=100, verbose_name='Cargo')

    class Meta:
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'

    def __str__(self):
        return f'{self.cargo}'


class Funcionario(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Usuário')
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, verbose_name='Cargo')
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, verbose_name='Setor')

    class Meta:
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'
    
    def __str__(self):
        return self.user.username
    
