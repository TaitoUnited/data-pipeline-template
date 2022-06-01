from rest_framework import serializers
from .models import Sales, SalesCreate


class SaleReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ("key", "order_number", "quantity", "price")


class SaleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesCreate
        fields = ("order_number", "quantity", "price")


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = "__all__"
