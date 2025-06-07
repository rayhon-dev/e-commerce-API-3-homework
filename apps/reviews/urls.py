from django.urls import path
from . import views


urlpatterns = [
    path('products/<int:pk>/reviews/', views.ReviewCreateView.as_view(), name='create')
]