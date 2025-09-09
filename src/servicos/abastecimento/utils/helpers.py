

def reverter_reabastecimento(obj):
    """
     Reverte um reabastecimento removendo a quantidade do tanque.
    """

    tanque = obj.tanque

    tanque.quantidade_disponivel -= obj.quantidade

    if tanque.quantidade_disponivel < 0:

        tanque.quantidade = 0

    tanque.save()
