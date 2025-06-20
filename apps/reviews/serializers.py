from rest_framework import serializers
from .models import Review
from users.models import User


class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name']
        read_only_fields = ['id', 'full_name']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    product_id = serializers.IntegerField(source='product.id', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product_id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'created_at', 'user', 'product_id']

    def create(self, validated_data):
        user = self.context['request'].user
        product = self.context['product']
        return Review.objects.create(user=user, product=product, **validated_data)

    def validate(self, attrs):
        user = self.context['request'].user
        product = self.context['product']

        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Siz bu mahsulotga allaqachon izoh yozgansiz.")

        return attrs
