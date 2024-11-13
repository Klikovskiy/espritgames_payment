from django.apps import AppConfig


class WalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'wallet'
    verbose_name = 'Баланс пользователей'

    def ready(self):
        import wallet.signals
