from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer
from common.pagination import CustomPagination
from rest_framework.permissions import IsAuthenticated


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_time')


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
