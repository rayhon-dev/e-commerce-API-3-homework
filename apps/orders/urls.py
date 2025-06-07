from django.urls import path
from . import views


urlpatterns = [
    path('orders/', views.OrderListCreateView.as_view(), name='list-create'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='detail')
]