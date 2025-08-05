from django.db import models

class Base(models.Model):
    criado = models.DateField(verbose_name='Criado', auto_now_add=True)
    modificado = models.DateTimeField(verbose_name='Atualizado', auto_now=True)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    class Meta:
        abstract = True

