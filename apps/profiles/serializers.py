from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='full_name')
    default_shipping_address = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id',
            'phone',
            'name',
            'email',
            'default_shipping_address',
            'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']