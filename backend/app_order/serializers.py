from rest_framework import serializers
from .models import Order, OrderItem
from app_catalog.serializers import ProductVariantSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = OrderItem
        fields = ['id', 'product_variant', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'first_name', 'last_name', 'email', 'phone', 
            'address', 'delivery_option', 'order_items', 'total_amount', 
            'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_amount', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    delivery_option_id = serializers.IntegerField()
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializers.CharField(max_length=20)
    address = serializers.CharField()

    def create(self, validated_data):
        # Логика создания заказа будет реализована в представлении
        pass
