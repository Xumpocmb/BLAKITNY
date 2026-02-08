from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import Http404
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer
from .logic import create_order_from_cart, get_user_orders, get_order_details, update_order_status, cancel_order
from app_cart.models import Cart


class OrderListView(generics.ListAPIView):
    """
    Представление для получения списка заказов пользователя.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return get_user_orders(self.request.user)


class OrderDetailView(generics.RetrieveAPIView):
    """
    Представление для получения деталей конкретного заказа.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        order_id = self.kwargs.get('pk')
        order = get_order_details(order_id)
        if not order:
            raise Http404("Заказ не найден")
        # Проверяем, принадлежит ли заказ текущему пользователю
        if order.user != self.request.user:
            raise Http404("Заказ не найден")
        return order


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_order(request):
    """
    Создает новый заказ из корзины пользователя.
    
    Args:
        request: HTTP-запрос с данными для создания заказа
        
    Returns:
        Response: JSON-ответ с созданным заказом или ошибкой
    """
    serializer = CreateOrderSerializer(data=request.data)
    if serializer.is_valid():
        # Получаем корзину пользователя
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response(
                {'error': 'Корзина пользователя не найдена'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not cart.items.exists():
            return Response(
                {'error': 'Корзина пуста'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Получаем данные из валидированного сериализатора
        delivery_option_id = serializer.validated_data['delivery_option_id']
        first_name = serializer.validated_data['first_name']
        last_name = serializer.validated_data['last_name']
        email = serializer.validated_data['email']
        phone = serializer.validated_data['phone']
        address = serializer.validated_data['address']
        
        try:
            order = create_order_from_cart(
                user=request.user,
                cart=cart,
                delivery_option_id=delivery_option_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address
            )
            
            order_serializer = OrderSerializer(order)
            return Response(order_serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': f'Ошибка при создании заказа: {str(e)}'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status_view(request, pk):
    """
    Обновляет статус заказа.
    
    Args:
        request: HTTP-запрос с новым статусом
        pk: ID заказа
        
    Returns:
        Response: JSON-ответ с результатом операции
    """
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response(
            {'error': 'Заказ не найден'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Проверяем, принадлежит ли заказ текущему пользователю
    if order.user != request.user:
        return Response(
            {'error': 'У вас нет прав для изменения этого заказа'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    new_status = request.data.get('status')
    if not new_status:
        return Response(
            {'error': 'Статус не указан'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    success = update_order_status(pk, new_status)
    if success:
        return Response({'message': 'Статус заказа успешно обновлен'})
    else:
        return Response(
            {'error': 'Недопустимый статус заказа'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def cancel_order_view(request, pk):
    """
    Отменяет заказ.
    
    Args:
        request: HTTP-запрос
        pk: ID заказа
        
    Returns:
        Response: JSON-ответ с результатом операции
    """
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response(
            {'error': 'Заказ не найден'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    
    # Проверяем, принадлежит ли заказ текущему пользователю
    if order.user != request.user:
        return Response(
            {'error': 'У вас нет прав для отмены этого заказа'}, 
            status=status.HTTP_403_FORBIDDEN
        )
    
    success = cancel_order(pk)
    if success:
        return Response({'message': 'Заказ успешно отменен'})
    else:
        return Response(
            {'error': 'Не удалось отменить заказ'}, 
            status=status.HTTP_400_BAD_REQUEST
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order_stats(request):
    """
    Возвращает статистику по заказам пользователя.
    
    Args:
        request: HTTP-запрос
        
    Returns:
        Response: JSON-ответ со статистикой
    """
    orders = get_user_orders(request.user)
    stats = {
        'total_orders': orders.count(),
        'pending_orders': orders.filter(status='pending').count(),
        'confirmed_orders': orders.filter(status='confirmed').count(),
        'processing_orders': orders.filter(status='processing').count(),
        'shipped_orders': orders.filter(status='shipped').count(),
        'delivered_orders': orders.filter(status='delivered').count(),
        'cancelled_orders': orders.filter(status='cancelled').count(),
    }
    return Response(stats)