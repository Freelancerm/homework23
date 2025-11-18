from rest_framework import serializers
from .models import Product, Review


# Вкладений серіалізатор
class ReviewSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для моделі Review.

    Використовується як вкладений (nested) серіалізатор у ProductSerializer
    для відображення пов'язаних відгуків.
    """
    class Meta:
        model = Review
        fields = ('id', 'text', 'rating')


class ProductSerializer(serializers.ModelSerializer):
    """
    Серіалізатор для моделі Product.

    Використовується для перетворення об'єктів Product на формати,
    придатні для API (JSON/XML), і навпаки.

    Включає вкладене поле `reviews` для відображення всіх відгуків,
    пов'язаних із продуктом.
    """
    # Вкладене поле (Related field)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'details', 'is_active', 'reviews')
