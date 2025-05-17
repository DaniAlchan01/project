from django.apps import AppConfig

class SourceprogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'SourceProg'

    def ready(self):
        import SourceProg.signals  # Подключаем сигналы при старте
