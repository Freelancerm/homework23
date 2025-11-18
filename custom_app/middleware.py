import time
from django.db import connection

# Зберігаємо кількість запитів у пам'яті
REQUEST_COUNTER = 0


# Middleware (кастомний заголовок). Метрики (час виконання, кількість запитів)
class CustomMetricsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global REQUEST_COUNTER
        REQUEST_COUNTER += 1  # Лічильник запитів

        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()

        # Додаємо кастомний заголовок
        response['X-Custom-Power'] = 'Powered-By-Django-Custom-Code'

        # Додаємо метрики дл заголовків
        response['X-Request-Count'] = str(REQUEST_COUNTER)
        response['X-Response-Time-Ms'] = f'{(end_time - start_time) * 1000:.2f}'

        # Метрики: кількість SQL-запитів
        if connection.queries:
            response['X-DB-Queries'] = str(len(connection.queries))

        return response
