from django.db import models


class UpperCaseCharField(models.CharField):
    """ Поле, яке зберігає текст у верхньому регістрі. """

    def pre_save(self, model_instance, add):
        value = super().pre_save(model_instance, add)
        if value:
            return value.upper()
        return value
