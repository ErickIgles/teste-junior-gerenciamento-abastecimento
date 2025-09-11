from django.db.models.signals import (
    pre_save,
    post_save,
    post_delete
)

from django.dispatch import receiver

from ..models import RegistroAbastecimento, RegistroReabastecimento


# Abastecimento

@receiver(pre_save, sender=RegistroAbastecimento)
def guardar_valor_antigo_abastecimento(sender, instance, **kwargs):
    print("🚀 Signal de guardar executado!")

    if instance.pk:

        antigo = sender.objects.get(pk=instance.pk)

        instance._antigo_litros = antigo.litros_abastecido

    else:

        instance._antigo_litros = 0


@receiver(post_save, sender=RegistroAbastecimento)
def atualizar_estoque_abastecimento(sender, instance, created, **kwargs):
    print("🚀 Signal de atualizar abastecimento executado!")
    tanque = instance.tanque

    if created:

        tanque.quantidade_disponivel -= instance.litros_abastecido

    else:

        diferenca = instance.litros_abastecido - instance._antigo_litros

        tanque.quantidade_disponivel -= diferenca

    tanque.save()


@receiver(post_delete, sender=RegistroAbastecimento)
def devolver_estoque_abastecimento(sender, instance, **kwargs):
    print("🚀 Signal de devolver abastecimento executado!")

    tanque = instance.tanque

    tanque.quantidade_disponivel += instance.litros_abastecido

    tanque.save()


# Reabastecimento
@receiver(pre_save, sender=RegistroReabastecimento)
def guardar_valor_antigo_reabastecimento(sender, instance, **kwargs):
    if instance.pk:
        antigo = sender.objects.get(pk=instance.pk)
        instance._antiga_quantidade = antigo.quantidade
    else:
        instance._antiga_quantidade = 0


@receiver(post_save, sender=RegistroReabastecimento)
def atualizar_estoque_reabastecimento(sender, instance, created, **kwargs):
    print("🚀 Signal de atualizar reabastecimento executado!")

    tanque = instance.tanque

    if created:

        tanque.quantidade_disponivel += instance.quantidade

    else:

        diferenca = instance.quantidade - instance._antiga_quantidade

        tanque.quantidade_disponivel += diferenca

        tanque.save()


@receiver(post_delete, sender=RegistroReabastecimento)
def remover_estoque_reabastecimento(sender, instance, **kwargs):
    print("🚀 Signal de remover estoque de reabastecimento executado!")

    tanque = instance.tanque

    tanque.quantidade_disponivel -= instance.quantidade

    tanque.save()
