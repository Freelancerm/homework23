from rest_framework import permissions


# Кастомний дозвіл
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Дозволяє читання (GET, HEAD, OPTIONS) усім, але запис (POST, PUT, DELETE)
    лише для адміністраторів (is_staff=True).
    """

    def has_permission(self, request, view):
        # Дозволити READ (безпечні методи)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Дозволити WRITE лише для адміністратора
        return request.user and request.user.is_staff
