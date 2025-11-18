from rest_framework import permissions


# Кастомний дозвіл
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Кастомний дозвіл для Django REST Framework (DRF).

    Дозволяє доступ до читання (READ) для будь-якого користувача,
    але обмежує доступ до запису/зміни (WRITE) лише для користувачів
    зі статусом адміністратора (`is_staff=True`).

    Використовується для захисту API-ендпоїнтів, де потрібна лише
    можливість перегляду для широкої публіки, але редагування
    доступне лише персоналу.
    """

    def has_permission(self, request, view):
        """
        Перевіряє, чи має користувач загальний дозвіл на виконання
        операції (на рівні всього представлення/view).

        1. **READ Access:** Якщо метод запиту належить до безпечних
           (GET, HEAD, OPTIONS), доступ дозволено.
        2. **WRITE Access:** Якщо метод не є безпечним (наприклад, POST, PUT, DELETE),
           дозвіл надається лише за умови, що користувач є аутентифікованим
           (`request.user`) та має статус персоналу (`request.user.is_staff`).

        :param request: Об'єкт Request.
        :param view: Об'єкт View, до якого застосовується дозвіл.
        :return: True, якщо дозвіл надано, інакше False.

        """
        # Дозволити READ (безпечні методи)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Дозволити WRITE лише для адміністратора
        return request.user and request.user.is_staff
