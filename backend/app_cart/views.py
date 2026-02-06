from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, AddToCartSerializer, CartItemSerializer
from app_catalog.models import ProductVariant


class CartDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получить, обновить или удалить корзину текущего пользователя
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    """
    Добавить товар в корзину
    """
    serializer = AddToCartSerializer(data=request.data)
    if serializer.is_valid():
        product_variant_id = serializer.validated_data['product_variant_id']
        quantity = serializer.validated_data['quantity']
        
        try:
            product_variant = ProductVariant.objects.get(id=product_variant_id, is_active=True)
        except ProductVariant.DoesNotExist:
            return Response({'error': 'Вариант товара не найден'}, status=status.HTTP_404_NOT_FOUND)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        # Проверяем, есть ли уже этот вариант в корзине
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant=product_variant,
            defaults={'quantity': quantity}
        )
        
        if not created:
            # Если элемент уже существует, увеличиваем количество
            cart_item.quantity += quantity
            cart_item.save()
        
        return Response({'message': 'Товар добавлен в корзину'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request, item_id):
    """
    Удалить конкретный элемент из корзины
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    cart_item.delete()
    return Response({'message': 'Товар удален из корзины'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_cart_item(request, item_id):
    """
    Обновить количество товара в корзине
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    quantity = request.data.get('quantity')
    if quantity is None:
        return Response({'error': 'Количество не указано'}, status=status.HTTP_400_BAD_REQUEST)
    
    if quantity <= 0:
        cart_item.delete()
        return Response({'message': 'Товар удален из корзины'}, status=status.HTTP_200_OK)
    
    cart_item.quantity = quantity
    cart_item.save()
    
    serializer = CartItemSerializer(cart_item)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    """
    Очистить всю корзину
    """
    cart = get_object_or_404(Cart, user=request.user)
    cart.items.all().delete()
    return Response({'message': 'Корзина очищена'}, status=status.HTTP_204_NO_CONTENT)
