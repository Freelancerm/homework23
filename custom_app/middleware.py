import time
from django.db import connection

# Зберігаємо кількість запитів у пам'яті
REQUEST_COUNTER = 0


# Middleware (кастомний заголовок). Метрики (час виконання, кількість запитів)
class CustomMetricsMiddleware:
    """
    Middleware, який додає до HTTP-відповіді (Response) кастомні заголовки
    з метриками продуктивності:

    1. Час виконання запиту (`X-Response-Time-Ms`).
    2. Загальна кількість HTTP-запитів до сервера з моменту запуску (`X-Request-Count`).
    3. Кількість SQL-запитів, виконаних під час обробки (`X-DB-Queries`).
    4. Кастомний ідентифікаційний заголовок (`X-Custom-Power`).
    """
    def __init__(self, get_response):
        """
        Ініціалізація Middleware.

        Зберігає функцію get_response, яка є наступним елементом
        у ланцюжку обробки Middleware або функцією представлення (view).

        :param get_response: Функція, яка викликається для отримання відповіді.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Виконується для кожного запиту перед викликом view та після
        отримання відповіді від view.

        1. Інкрементує глобальний лічильник запитів.
        2. Записує час початку виконання.
        3. Викликає наступний елемент ланцюжка для отримання відповіді.
        4. Записує час завершення та обчислює різницю.
        5. Додає метрики та кастомні заголовки до об'єкта відповіді.

        :param request: Об'єкт HttpRequest.
        :return: Об'єкт HttpResponse з доданими заголовками.
        """
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
