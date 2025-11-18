from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.views import View
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductSerializer
from .permissions import IsAdminOrReadOnly
from .models import Product
from .forms import ProductForm

from django.db.models import Count, Q

# Кастомні запити через ORM
# Кастомний запит через ORM: Знайти активні продукти, які мають більше 10 відгуків
high_rated_products = Product.objects.filter(is_active=True).annotate(
    review_count=Count('reviews')
).filter(review_count__gt=10)
"""
ORM-запит: Знайти активні продукти (`is_active=True`),
які мають більше 10 відгуків.

Використовує:
1. `filter()` для фільтрації за полем моделі.
2. `annotate()` для обчислення агрегованого значення (`review_count` - кількість відгуків).
3. `filter()` для фільтрації за обчисленим значенням (`review_count__gt=10`).
"""

# Продукти, назва яких починається з "A" або "B"
filtered_products = Product.objects.filter(
    Q(name__startswith='A') | Q(name__startswith='B')
)
"""
ORM-запит: Знайти продукти, назва яких починається з 'A' АБО з 'B'.

Використовує:
1. Об'єкти `Q` для побудови складних логічних умов (оператор OR, `|`).
2. Оператор `__startswith` для пошуку за префіксом.
"""

def product_create_view(request):
    """
    Просте функціональне відображення для відображення форми створення продукту.

    :param request: Об'єкт HttpRequest.
    :return: Об'єкт HttpResponse, що рендерить шаблон `product_form.html`.
    """
    form = ProductForm()
    return render(request, 'product_form.html', {'form': form})


# Кастомне класове відображення
class HomePageView(TemplateView):
    """
    Класове відображення на основі TemplateView.

    Використовується для відображення статичної сторінки з додаванням
    кастомних даних у контекст.
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        """
        Розширює стандартний контекст, додаючи кастомне повідомлення.

        :param kwargs: Додаткові ключові аргументи.
        :return: Словник контексту, який буде передано до шаблону.
        """
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ласкаво просимо до мого кастомного відображення!'
        return context


# Класове відображення для обробки форми
from django.template.loader import get_template
class ProductCreateView(View):
    """
    Класове відображення на основі базового View для обробки форми створення продукту.

    Обробляє GET-запит (відображення форми) та POST-запит (валідація та збереження форми).
    """
    def get(self, request):
        """
        Обробляє GET-запит: ініціалізує та відображає порожню форму.

        :return: HttpResponse з формою.
        """
        form = ProductForm()
        return render(request, 'product_form.html', {'form': form})

    def post(self, request):
        """
        Обробляє POST-запит: валідує дані та зберігає продукт.

        Якщо форма дійсна, зберігає об'єкт і перенаправляє користувача.
        Якщо недійсна, повторно відображає форму з помилками.

        :return: HttpResponse (або редирект).
        """
        form = ProductForm(request.POST)
        if form.is_valid():
            # Тут спрацюють: UpperCaseCharField.pre_save та validate_no_bad_words
            product = form.save()
            color_code = form.cleaned_data.get('color_code')
            return redirect('home')  # Редирект на головну
        return render(request, 'product_form.html', {'form': form})


# Viewset із фільтрацією та кастомними дозволами
class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet для моделі Product.

    Забезпечує повний CRUD функціонал (Create, Retrieve, Update, Destroy)
    через єдиний клас.

    Налаштовано:
    1. Обмежений набір об'єктів (тільки активні).
    2. Попереднє завантаження пов'язаних об'єктів (`reviews`).
    3. Кастомні дозволи (тільки адміністратор може змінювати дані).
    4. Фільтрація за допомогою `DjangoFilterBackend`.
    """
    queryset = Product.objects.filter(is_active=True).prefetch_related('reviews')
    serializer_class = ProductSerializer

    # Кастомні дозволи
    permission_classes = [IsAdminOrReadOnly]

    # Фільтрація
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'is_active']
