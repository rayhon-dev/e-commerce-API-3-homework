from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from common.pagination import CustomPagination
from .serializers import ReviewSerializer
from products.models import Product

class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            product = Product.objects.get(id=self.kwargs['pk'])
        except Product.DoesNotExist:
            raise NotFound("Mahsulot topilmadi.")
        context['product'] = product
        return context
