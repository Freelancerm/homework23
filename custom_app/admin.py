from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Product, Review, CustomUser
from .forms import UserCreationForm, CustomUserCreationForm


# Реєструємо кастомну модель користувача
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Адмін-клас для кастомної моделі користувача CustomUser.

    Розширює стандартну функціональність, додаючи кастомні поля,
    такі як 'phone_number', і використовує спеціалізовані форми.
    """
    # Використовуємо кастомну форму для створення
    add_form = CustomUserCreationForm
    form = CustomUserCreationForm
    model = CustomUser
    list_display = ['username', 'email', 'phone_number', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        (('Кастомні поля'), {'fields': ('phone_number',)}),
    )


# Inline-моделі
class ReviewInline(admin.TabularInline):
    """
    Inline-клас для моделі Review.

    Дозволяє редагувати відгуки (Review) безпосередньо на сторінці
    редагування пов'язаного об'єкта Product.
    """
    model = Review
    extra = 1
    # Обмеження полів для відображення
    fields = ('text', 'rating')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Адмін-клас для моделі Product.

    Налаштовує відображення, фільтрацію, пошук, додає inline-віджети
    для відгуків та реєструє кастомні дії.
    """
    # Кастомні list_display (включаючи методи моделі)
    list_display = ('name', 'is_active', 'created_at', 'get_name_length', 'count_details_keys')

    # Фільтри
    list_filter = ('is_active', 'created_at',)
    search_fields = ('name',)

    # Inline
    inlines = [ReviewInline]

    # Кастомні дії
    actions = ['set_inactive', 'make_names_uppercase']

    @admin.action(description='Зробити вибрані продукти неактивними')
    def set_inactive(self, request, queryset):
        """
        Кастомна дія: Встановлює поле `is_active` у `False` для вибраних об'єктів.
        """
        updated = queryset.update(is_active=False)
        self.message_user(request, f'Зроблено неактивними {updated} продуктів.')

    @admin.action(description='Перетворити імена на UPPERCASE')
    def makes_names_uppercase(self, request, queryset):
        """
        Кастомна дія: Зберігає кожен вибраний об'єкт.

        Примітка: Припускається, що метод `save()` моделі Product містить
        логіку, яка автоматично перетворює ім'я (name) на верхній регістр
        або виконує іншу необхідну обробку.
        """
        for obj in queryset:
            obj.save()
        self.message_user(request, f'Оновлено {queryset.count()} продуктів.')
