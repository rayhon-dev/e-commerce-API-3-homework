from rest_framework import generics, permissions
from common.pagination import CustomPagination
from .models import Review
from .serializers import ReviewSerializer
from products.models import Product
from rest_framework.exceptions import ValidationError

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        product = generics.get_object_or_404(Product, pk=self.kwargs['id'])
        context['product'] = product
        return context

    def perform_create(self, serializer):
        product = generics.get_object_or_404(Product, pk=self.kwargs['id'])
        user = self.request.user

        if Review.objects.filter(user=user, product=product).exists():
            raise ValidationError("Siz bu mahsulotga allaqachon sharh qoldirgansiz.")

        serializer.save(user=user, product=product)
