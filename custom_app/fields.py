from django.db import models


class UpperCaseCharField(models.CharField):
    """
    Кастомне поле CharField, яке автоматично перетворює вхідний текст
    на **верхній регістр (UPPERCASE)** перед збереженням у базу даних.

    Наслідує стандартний функціонал `models.CharField`.

    Метод `pre_save` гарантує, що значення буде перетворено перед
    виконанням будь-яких операцій INSERT або UPDATE.
    """

    def pre_save(self, model_instance, add):
        """
        Обробляє значення перед його збереженням у базу даних.

        1. Отримує поточне значення від базового класу.
        2. Якщо значення не є порожнім, перетворює його на верхній регістр.
        3. Повертає оброблене значення для збереження.

        :param model_instance: Екземпляр моделі, який зберігається.
        :param add: Булеве значення; True, якщо це новий об'єкт (INSERT),
                    False, якщо це оновлення існуючого (UPDATE).
        :return: Значення, яке буде збережено в полі бази даних.
        :rtype: str або None
        """
        value = super().pre_save(model_instance, add)
        if value:
            return value.upper()
        return value
