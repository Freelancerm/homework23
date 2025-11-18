from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import re
from .models import Product, CustomUser


# --- Кастомний фільтр ---
def validate_no_bad_words(value):
    """
    Кастомний валідатор, який перевіряє, чи містить рядок заборонені слова.

    Порівняння виконується без урахування регістру.

    :param value: Рядок (str), який потрібно перевірити.
    :raises ValidationError: Якщо у рядку знайдено одне або кілька заборонених слів.
    """
    bad_words = ['spam', 'badword', 'forbidden']
    if any(word in value.lower() for word in bad_words):
        raise ValidationError(f'Поле містить заборонені слова: {value}')


# --- Кастомний віджет ---
class CustomSelectWidget(forms.Select):
    """
    Кастомний віджет на основі forms.Select.

    Використовує власний шаблон для відображення (`widgets/custom_select.html`)
    та додає кастомний атрибут до контексту віджета.
    """
    template_name = 'widgets/custom_select.html'

    def get_context(self, name, value, attrs):
        """
        Розширює стандартний контекст віджета, додаючи кастомний атрибут.

        :param name: Назва поля.
        :param value: Поточне значення поля.
        :param attrs: Словник HTML-атрибутів.
        :return: Словник контексту для рендерингу віджета у шаблоні.
        """
        context = super().get_context(name, value, attrs)
        context['widget']['custom_attr'] = 'my-custom-select-class'
        return context


# --- Кастомне поле форми ---
class HexCodeField(forms.CharField):
    """
    Кастомне поле форми для валідації HEX-коду кольору.

    Забезпечує перетворення вхідного значення (прибирає '#', перетворює на UPPERCASE)
    та перевіряє відповідність формату HEX-коду (6 або 3 символи).
    """

    def to_python(self, value):
        """
        Конвертує вхідне значення у відповідний тип (str) та нормалізує його.

        Видаляє можливий префікс '#' та перетворює рядок на верхній регістр.

        :param value: Вхідне значення поля.
        :return: Нормалізований рядок HEX-коду або None.
        """
        value = super().to_python(value)
        if value is None:
            return None
        # Видаляємо можливий '#' та перетворюємо на верхній регістр
        return value.lstrip('#').upper()

    def validate(self, value):
        """
        Виконує валідацію нормалізованого значення.

        Перевіряє, чи відповідає рядок формату HEX-коду (6 або 3 символи, A-F, 0-9).

        :param value: Нормалізоване значення поля (без '#', у верхньому регістрі).
        :raises forms.ValidationError: Якщо формат HEX-коду недійсний.
        """
        super().validate(value)
        hex_regex = re.compile(r'^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
        if not hex_regex.match(value):
            raise forms.ValidationError('Введіть дійсний HEX-код кольору (наприклад, FF00AA або F0A).')


# --- Форма з кастомною валідацією та віджетом ---
class ProductForm(forms.ModelForm):
    """
    Форма моделі для Product.

    Використовує кастомне поле `HexCodeField` для кольору,
    кастомний віджет `CustomSelectWidget` для поля `details`
    та містить кастомну валідацію поля `name` за допомогою `validate_no_bad_words`.
    """
    # Додаємо кастомне поле форми
    color_code = HexCodeField(required=False, help_text="Код кольору продукту")

    class Meta:
        model = Product
        fields = ('name', 'details')
        widgets = {
            'details': CustomSelectWidget(choices=[('A', 'Type A'), ('B', 'Type B')]),
        }

    def clean_name(self):
        """
        Метод очищення (валідації) для поля `name`.

        Викликає глобальний валідатор `validate_no_bad_words` для перевірки
        на заборонені слова.
        :return: Очищене значення поля `name`.
        """
        # Використання кастомного валідатора
        name = self.cleaned_data['name']
        validate_no_bad_words(name)
        return name


# --- Форма реєстрації з кастомною валідацією ---
class CustomUserCreationForm(UserCreationForm):
    """
    Кастомна форма реєстрації користувачів.

    Наслідує стандартну `UserCreationForm` і додає кастомну валідацію
    для поля `phone_number`.
    """
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')

    def clean_phone_number(self):
        """
        Метод очищення (валідації) для поля `phone_number`.

        Виконує перевірку формату номера телефону на відповідність
        міжнародному формату (наприклад, `+380...`).

        :return: Очищене значення поля `phone_number` або None.
        :raises forms.ValidationError: Якщо номер не відповідає формату.
        """
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number:
            # Кастомна валідація формату (+380.....)
            phone_regex = re.compile(r'^\+\d{10,15}$')
            if not phone_regex.match(phone_number):
                raise forms.ValidationError("Номер повинен бути у міжнародному форматі")
            return phone_number

        # Повертаємо None, якщо поле було порожнім і валідація не потрібна
        return phone_number
