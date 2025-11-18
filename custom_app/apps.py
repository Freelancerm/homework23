from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_app'

    def ready(self):
        # Підключення сигналів
        import custom_app.signals
