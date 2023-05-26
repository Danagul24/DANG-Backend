from rest_framework import serializers
from .models import Category, Item


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = ["name", "description", "category", "UOM", "price", "discount", "city", "created_at"]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
