from rest_framework import serializers
from .models import Product, Like, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'name',
            'slug'
        ]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    average_rating = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'price',
            'thumbnail',
            'category',
            'average_rating',
            'likes_count'
        ]

    # def get_average_rating(self, obj):
    #     return obj.likes.count()


    def get_likes_count(self, obj):
        return obj.likes.count()



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = [
            'id',
            'product'
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']
        like, created = Like.objects.get_or_create(user=user, product=product)
        if not created:
            like.delete()
            return None
        return like
