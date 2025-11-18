from django.db import models
from django.contrib.auth.models import AbstractUser
from .fields import UpperCaseCharField
import json


# Кастомна модель користувача
class CustomUser(AbstractUser):
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
        related_name="custom_user_set",  # <--- УНІКАЛЬНА НАЗВА
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="custom_user_permissions_set",  # <--- УНІКАЛЬНА НАЗВА
        related_query_name="custom_user_permission",
    )
    # ========================

    def __str__(self):
        return self.username


class Product(models.Model):
    # Кастомне поле для зберігання у верхньому регістрі
    name = UpperCaseCharField(max_length=100)

    # Зберігання даних у форматі JSON
    details = models.JSONField(default=dict)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Метод обробки даних(підрахунок статистики)
    def get_name_length(self):
        """ Повертає довжину назви продукту. """
        return len(self.name)

    def count_details_keys(self):
        """ Підраховує кількість ключів у JSON полі 'details'. """
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

    def __str__(self):
        return self.name


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='рейтинг')
    text = models.TextField()
    rating = models.IntegerField(default=5)

    def __str__(self):
        return f"Рейтинг продукту {self.product.name} ({self.rating}/5)"
