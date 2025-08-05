from django.db import models



class Base(models.Model):
    criado = models.DateField(verbose_name='Criado', auto_now_add=True)
    modificado = models.DateTimeField(verbose_name='Atualizado', auto_now=True)
    ativo = models.BooleanField(verbose_name='Ativo', default=True)

    class Meta:
        abstract = True


class Tanque(Base):
    TIPO_COMBUSTIVEL_CHOICES = [
        ('GASOLINA', 'Gasolina'),
        ('DIESEL', 'Óleo Diesel')
    ]

    tipo_combustivel = models.CharField(verbose_name='Combustivel', max_length=10, choices=TIPO_COMBUSTIVEL_CHOICES)
    quantidade = models.IntegerField(verbose_name='Quantidade')

    class Meta:
        verbose_name = 'Tanque'
        verbose_name_plural = 'Tanques'
    
    def __str__(self):
        return f'{self.tipo_combustivel} {self.quantidade}'


class Bomba(Base):
    nome_bomba = models.CharField(verbose_name='Nome', max_length=144)
    tanque = models.ForeignKey(Tanque, verbose_name='Tanque', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Bomba'
        verbose_name_plural = 'Bombas'
    
    def __str__(self):
        return f'{self.nome_bomba} {self.tanque}'
    

class Abastecimento(Base):
    bomba = models.ForeignKey(Bomba, verbose_name='Bomba', on_delete=models.CASCADE)
    litros_abastecidos = models.IntegerField(verbose_name='Litros abastecidos')
    valor = models.DecimalField(verbose_name='Valor', max_digits=8 ,decimal_places=2)

    class Meta:
        verbose_name = 'Abastecimento'
        verbose_name_plural = 'Abastecimentos'
    
    
    def save(self, *args, **kwargs):
        self.valor = self.valor + ((self.valor * 13)/100)
        return super().save(*args, **kwargs)
    
    @property
    def falta_abastecer(self):
        return self.bomba.tanque.quantidade - self.litros_abastecidos
    
    def __str__(self):
        return f'Abastecimento na {self.bomba.nome_bomba}: {self.litros_abastecidos}L - R${self.valor}'
    

