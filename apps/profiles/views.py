from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from .serializers import UserProfileSerializer
from common.pagination import CustomPagination


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_object(self):
        try:
            return self.request.user.profile
        except Exception:
            raise NotFound("Foydalanuvchining profili mavjud emas")

