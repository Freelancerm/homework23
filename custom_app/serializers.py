from rest_framework import serializers
from .models import Product, Review


# Вкладений серіалізатор
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'rating')


class ProductSerializer(serializers.ModelSerializer):
    # Вкладене поле (Related field)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('id', 'name', 'details', 'is_active', 'reviews')
