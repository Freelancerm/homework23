from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
import logging

# Використовуємо кастомний логгер
logger = logging.getLogger('custom_app_logger')


# Сигнал post_save
@receiver(post_save, sender=Product)
def product_post_save_handler(sender, instance, created, **kwargs):
    if created:
        message = f"Новий продукт '{instance.name}' (ID: {instance.id}) створено."

        # Логування
        logger.info(message)
    else:
        message = f"Продукт '{instance.name}' (ID: {instance.id}) оновлено."
