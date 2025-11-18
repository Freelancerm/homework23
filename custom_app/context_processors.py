from datetime import datetime


# Кастомний контекстний процесор
def global_settings(request):
    """ Передає глобальні дані у кожен шаблон. """
    return {
        'SITE_NAME': 'Мій кастомний проект Django',
        'CURRENT_YEAR': datetime.now().year,
    }
