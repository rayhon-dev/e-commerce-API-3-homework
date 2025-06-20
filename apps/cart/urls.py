from django.urls import path
from . import views


urlpatterns = [
    path('cart/', views.CartListCreateView.as_view(), name='list-create'),
    path('cart/<int:product_id>/', views.CartItemDeleteView.as_view(), name='delete-cart-item'),
]