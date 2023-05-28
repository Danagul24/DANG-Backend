from rest_framework import serializers
from .models import Category, Item


class ItemSerializer(serializers.ModelSerializer):
    expiry_date = serializers.DateField(format="%d.%m.%Y")

    class Meta:
        model = Item
        fields = ["id", "name", "description", "category", "UOM", "price", "discount", "expiry_date", "city", "created_at"]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"
