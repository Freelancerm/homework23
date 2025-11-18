from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
import logging

# Використовуємо кастомний логгер
logger = logging.getLogger('custom_app_logger')


# Сигнал post_save
@receiver(post_save, sender=Product)
def product_post_save_handler(sender, instance, created, **kwargs):
    """
    Обробник сигналу `post_save` для моделі Product.

    Ця функція автоматично викликається щоразу, коли об'єкт Product
    зберігається (створюється або оновлюється) у базі даних.

    Виконує логування події створення або оновлення продукту.

    :param sender: Клас моделі, що надіслала сигнал (тут це Product).
    :param instance: Фактичний екземпляр моделі, який був збережений.
    :param created: Булеве значення; True, якщо об'єкт було створено,
                    False, якщо його було оновлено.
    :param kwargs: Додаткові ключові аргументи.
    """
    if created:
        message = f"Новий продукт '{instance.name}' (ID: {instance.id}) створено."

        # Логування
        logger.info(message)
    else:
        message = f"Продукт '{instance.name}' (ID: {instance.id}) оновлено."
