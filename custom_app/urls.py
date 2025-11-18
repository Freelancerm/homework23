from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HomePageView, ProductViewSet, ProductCreateView


router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('api/', include(router.urls)),
]