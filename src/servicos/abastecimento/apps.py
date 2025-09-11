from django.apps import AppConfig


class AbastecimentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'servicos.abastecimento'

    def ready(self):

        import servicos.abastecimento.utils.signals
