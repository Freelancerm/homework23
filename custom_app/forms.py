from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
import re
from .models import Product, CustomUser


# --- Кастомний фільтр ---
def validate_no_bad_words(value):
    bad_words = ['spam', 'badword', 'forbidden']
    if any(word in value.lower() for word in bad_words):
        raise ValidationError(f'Поле містить заборонені слова: {value}')


# --- Кастомний віджет ---
class CustomSelectWidget(forms.Select):
    template_name = 'widgets/custom_select.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['custom_attr'] = 'my-custom-select-class'
        return context


# --- Кастомне поле форми ---
class HexCodeField(forms.CharField):
    """ Поле для валідації HEX-коду кольору. """

    def to_python(self, value):
        value = super().to_python(value)
        if value is None:
            return None
        # Видаляємо можливий '#' та перетворюємо на верхній регістр
        return value.lstrip('#').upper()

    def validate(self, value):
        super().validate(value)
        hex_regex = re.compile(r'^([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
        if not hex_regex.match(value):
            raise forms.ValidationError('Введіть дійсний HEX-код кольору (наприклад, FF00AA або F0A).')


# --- Форма з кастомною валідацією та віджетом ---
class ProductForm(forms.ModelForm):
    # Додаємо кастомне поле форми
    color_code = HexCodeField(required=False, help_text="Код кольору продукту")

    class Meta:
        model = Product
        fields = ('name', 'details')
        widgets = {
            'details': CustomSelectWidget(choices=[('A', 'Type A'), ('B', 'Type B')]),
        }

    def clean_name(self):
        # Використання кастомного валідатора
        name = self.cleaned_data['name']
        validate_no_bad_words(name)
        return name


# --- Форма реєстрації з кастомною валідацією ---
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')

        if phone_number:
            # Кастомна валідація формату (+380.....)
            phone_regex = re.compile(r'^\+\d{10,15}$')
            if not phone_regex.match(phone_number):
                raise forms.ValidationError("Номер повинен бути у міжнародному форматі")
            return phone_number

        # Повертаємо None, якщо поле було порожнім і валідація не потрібна
        return phone_number
