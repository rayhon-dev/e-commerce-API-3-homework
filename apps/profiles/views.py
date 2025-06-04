from rest_framework import generics, permissions
from .serializers import UserProfileSerializer
from common.pagination import CustomPagination


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_object(self):
        return self.request.user.profile
