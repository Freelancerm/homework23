from django.apps import AppConfig


class CustomAppConfig(AppConfig):
    """
    Конфігурація застосунку 'custom_app'.

    Цей клас визначає метадані та поведінку для Django-застосунку
    з назвою 'custom_app'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_app'

    def ready(self):
        """ Викликається, коли Django повністю завантажує реєстр застосунків.

        Використовується для виконання налаштувань при запуску, зокрема
        для підключення (імпорту) сигналів застосунку, щоб вони почали
        працювати.

        Примітка: Тут імпортується модуль signals, що ініціалізує визначені
        в ньому зв'язки (connect) сигналів.
        """
        import custom_app.signals
