from django.apps import AppConfig


class CuentasConfig(AppConfig):
    name = 'cuentas'

    def ready(self):
        from . import signals
