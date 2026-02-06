from rest_framework import serializers
from .models import Cart, CartItem
from app_catalog.serializers import ProductVariantSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product_variant', 'quantity', 'total_price']
        
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()
    total_items = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price', 'total_items', 'created_at', 'updated_at']


class AddToCartSerializer(serializers.Serializer):
    product_variant_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
    
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Количество должно быть больше 0")
        return value