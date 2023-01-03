"""
Product serializer for the API View.
"""
from django.utils.translation import gettext as _

from rest_framework import serializers

from core.models import Product


class ProductSerializer(serializers.ModelSerializer):
    # reviews = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = '__all__'

    # def get_reviews(self, obj):
    #     reviews = obj.review_set.all()
    #     serializer = ReviewSerializer(reviews, many=True)
    #     return serializer.data

class ProductImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to product."""

    class Meta:
        model = Product
        fields = ['id', 'image']
        read_only_fields = ['id']
        extra_kwargs = {'image': {'required': 'True'}}