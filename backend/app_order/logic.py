"""
Модуль содержит бизнес-логику для работы с заказами.
"""
from decimal import Decimal
from django.db import transaction
from django.contrib.auth.models import User
from app_order.models import Order, OrderItem
from app_cart.models import Cart
from app_home.models import DeliveryOption


def create_order_from_cart(user, cart, delivery_option_id, first_name, last_name, email, phone, address):
    """
    Создает заказ из содержимого корзины пользователя.
    
    Args:
        user: Пользователь, делающий заказ
        cart: Объект корзины
        delivery_option_id: ID выбранного варианта доставки
        first_name: Имя пользователя
        last_name: Фамилия пользователя
        email: Email пользователя
        phone: Номер телефона пользователя
        address: Адрес доставки
    
    Returns:
        Order: Созданный объект заказа
    """
    # Получаем вариант доставки
    delivery_option = DeliveryOption.objects.get(id=delivery_option_id)
    
    # Рассчитываем общую сумму заказа
    total_amount = cart.get_total_price()
    
    # Создаем заказ в транзакции
    with transaction.atomic():
        order = Order.objects.create(
            user=user if user.is_authenticated else None,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            delivery_option=delivery_option,
            total_amount=total_amount
        )
        
        # Создаем элементы заказа из содержимого корзины
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product_variant=cart_item.product_variant,
                quantity=cart_item.quantity,
                price=cart_item.product_variant.price
            )
        
        # Очищаем корзину после создания заказа
        cart.items.all().delete()
    
    return order


def update_order_status(order_id, new_status):
    """
    Обновляет статус заказа.
    
    Args:
        order_id: ID заказа
        new_status: Новый статус заказа
    
    Returns:
        bool: True, если статус успешно обновлен, иначе False
    """
    try:
        order = Order.objects.get(id=order_id)
        # Проверяем, является ли новый статус допустимым
        valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]
        if new_status in valid_statuses:
            order.status = new_status
            order.save(update_fields=['status', 'updated_at'])
            return True
        return False
    except Order.DoesNotExist:
        return False


def get_user_orders(user):
    """
    Возвращает все заказы пользователя.
    
    Args:
        user: Пользователь
    
    Returns:
        QuerySet: Заказы пользователя, отсортированные по дате создания (новые первыми)
    """
    return Order.objects.filter(user=user).order_by('-created_at')


def get_order_details(order_id):
    """
    Возвращает детали заказа по его ID.
    
    Args:
        order_id: ID заказа
    
    Returns:
        Order: Объект заказа или None, если заказ не найден
    """
    try:
        return Order.objects.prefetch_related('order_items__product_variant__product', 'order_items__product_variant__size').get(id=order_id)
    except Order.DoesNotExist:
        return None


def calculate_order_total(order):
    """
    Пересчитывает общую сумму заказа на основе его элементов.
    
    Args:
        order: Объект заказа
    
    Returns:
        Decimal: Общая сумма заказа
    """
    total = Decimal('0.00')
    for item in order.order_items.all():
        total += item.total_price
    return total


def cancel_order(order_id):
    """
    Отменяет заказ.
    
    Args:
        order_id: ID заказа
    
    Returns:
        bool: True, если заказ успешно отменен, иначе False
    """
    try:
        order = Order.objects.get(id=order_id)
        if order.status != 'cancelled':
            order.status = 'cancelled'
            order.save(update_fields=['status', 'updated_at'])
            return True
        return False
    except Order.DoesNotExist:
        return False


def get_orders_by_status(status):
    """
    Возвращает заказы с определенным статусом.
    
    Args:
        status: Статус заказа
    
    Returns:
        QuerySet: Заказы с указанным статусом
    """
    return Order.objects.filter(status=status)


def get_recent_orders(limit=10):
    """
    Возвращает недавние заказы.
    
    Args:
        limit: Количество заказов для возврата (по умолчанию 10)
    
    Returns:
        QuerySet: Последние заказы
    """
    return Order.objects.select_related('user', 'delivery_option').order_by('-created_at')[:limit]


def get_orders_statistics():
    """
    Возвращает статистику по заказам.
    
    Returns:
        dict: Словарь с количеством заказов по статусам
    """
    stats = {}
    for status, _ in Order.STATUS_CHOICES:
        stats[status] = Order.objects.filter(status=status).count()
    
    stats['total'] = Order.objects.count()
    stats['total_revenue'] = sum([order.total_amount for order in Order.objects.all()], Decimal('0.00'))
    
    return stats