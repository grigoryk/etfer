from django.apps import AppConfig


class EtfConfig(AppConfig):
    name = 'etf'

    def ready(self):
        from .signals import process_raw_data
