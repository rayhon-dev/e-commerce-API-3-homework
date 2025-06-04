from django.urls import path
from .views import ProductListView, ProductRetrieveView, ProductLikeToggleView

urlpatterns = [
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductRetrieveView.as_view(), name='product-detail'),
    path('products/<int:pk>/like/', ProductLikeToggleView.as_view(), name='product-like-toggle'),
]
