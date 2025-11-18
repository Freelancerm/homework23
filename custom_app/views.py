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

# Кастомний запит через ORM
# Знайти активні продукти, які мають більше 10 відгуків
high_rated_products = Product.objects.filter(is_active=True).annotate(
    review_count=Count('рейтинг')
).filter(review_count__gt=10)

# Продукти, назва яких починається з "A" або "B"
filtered_products = Product.objects.filter(
    Q(name__startswith='A') | Q(name__startswith='B')
)


def product_create_view(request):
    form = ProductForm()
    return render(request, 'product_form.html', {'form': form})


# Кастомне класове відображення
class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Ласкаво просимо до мого кастомного відображення!'
        return context


# Класове відображення для обробки форми
from django.template.loader import get_template
class ProductCreateView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'product_form.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            # Тут спрацюють: UpperCaseCharField.pre_save та validate_no_bad_words
            product = form.save()
            color_code = form.cleaned_data.get('color_code')
            return redirect('home')  # Редирект на головну
        return render(request, 'product_form.html', {'form': form})


# Viewset із фільтрацією та кастомними дозволами
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True).prefetch_related('reviews')
    serializer_class = ProductSerializer

    # Кастомні дозволи
    permission_classes = [IsAdminOrReadOnly]

    # Фільтрація
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'is_active']
