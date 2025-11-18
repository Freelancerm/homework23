from django.db import models
from django.contrib.auth.models import AbstractUser
from .fields import UpperCaseCharField
import json


# Кастомна модель користувача
class CustomUser(AbstractUser):
    """
    Кастомна модель користувача, що розширює стандартну модель `AbstractUser`.

    Додає поле `phone_number` та вирішує конфлікти `related_name`
    для полів `groups` та `user_permissions` при використанні кастомної
    моделі користувача.
    """
    phone_number = models.CharField(max_length=15, blank=True, null=True, unique=True)

    # === Виправлення конфлікту E304 ===
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="custom_user_permissions_set",
        related_query_name="custom_user_permission",
    )
    # ========================

    def __str__(self):
        """ Повертає рядок, що представляє об'єкт (username). """
        return self.username


class Product(models.Model):
    """
    Модель, що представляє продукт.

    Містить кастомне поле для назви у верхньому регістрі та
    поле JSON для гнучких деталей.
    """
    # Кастомне поле для зберігання у верхньому регістрі
    name = UpperCaseCharField(max_length=100)

    # Зберігання даних у форматі JSON
    details = models.JSONField(default=dict)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Метод обробки даних(підрахунок статистики)
    def get_name_length(self):
        """
        Повертає довжину назви продукту.

        Використовується в Django Admin для відображення додаткової інформації.
        :return: Довжина назви (int).
        """
        return len(self.name)

    def count_details_keys(self):
        """
        Підраховує кількість ключів/елементів у JSON полі 'details'.

        Обробляє випадки, коли поле може зберігатися як рядок JSON (наприклад,
        за певних умов або під час міграції) і намагається його десеріалізувати.

        :return: Кількість ключів у словнику або елементів у списку (int).
        """
        details_data = self.details

        # Перевірка: Якщо details — рядок, спробуйте його десеріалізувати
        if isinstance(details_data, str):
            try:
                # Намагаємося перетворити JSON-рядок на Python-об'єкт
                details_data = json.loads(details_data)
            except (json.JSONDecodeError, TypeError):
                # Якщо десеріалізація не вдалася або це пустий рядок/None
                return 0

        # Якщо це словник/список, повертаємо його довжину
        if isinstance(details_data, dict):
            return len(details_data.keys())
        elif isinstance(details_data, list):
            return len(details_data)

        # Якщо це щось інше (наприклад, None або пусте поле)
        return 0
    # Додавання атрибутів для відображення в Django Admin
    count_details_keys.short_description = 'К-ть деталей'

    def __str__(self):
        """ Повертає рядок, що представляє об'єкт (назва продукту). """
        return self.name


class Review(models.Model):
    """
    Модель для зберігання відгуків та рейтингів до продуктів.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    text = models.TextField()
    rating = models.IntegerField(default=5)

    def __str__(self):
        """ Повертає рядок, що представляє об'єкт (рейтинг і назва продукту). """
        return f"Рейтинг продукту {self.product.name} ({self.rating}/5)"
