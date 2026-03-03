from django.db import models
from django.conf import settings
from app_catalog.models import ProductVariant


class CartManager(models.Manager):
    def get_total_cost(self):
        """Возвращает общую стоимость всех товаров во всех корзинах"""
        from django.db.models import Sum, F
        return self.aggregate(
            total_cost=Sum(F('items__product_variant__price') * F('items__quantity'))
        )['total_cost'] or 0
    
    def get_total_items(self):
        """Возвращает общее количество товаров во всех корзинах"""
        from django.db.models import Sum
        return self.aggregate(
            total_items=Sum('items__quantity')
        )['total_items'] or 0


class Cart(models.Model):
    """
    Модель корзины покупок пользователя
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    objects = CartManager()

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина {self.user.username}'

    def get_total_price(self):
        """Общая стоимость всех товаров в корзине"""
        from django.db.models import Sum, F
        total = self.items.aggregate(
            total=Sum(F('product_variant__price') * F('quantity'))
        )['total']
        return total or 0

    def get_total_items(self):
        """Общее количество товаров в корзине"""
        from django.db.models import Sum
        total = self.items.aggregate(
            total=Sum('quantity')
        )['total']
        return total or 0
        
    @property
    def total_price(self):
        """Общая стоимость всех товаров в корзине (для совместимости)"""
        return self.get_total_price()

    @property
    def total_items(self):
        """Общее количество товаров в корзине (для совместимости)"""
        return self.get_total_items()


class CartItem(models.Model):
    """
    Элемент корзины - связывает корзину, товарный вариант и количество
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='Корзина')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name='Вариант товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'

    def __str__(self):
        return f'{self.quantity}x {self.product_variant.product.name} ({self.product_variant.size.name})'

    @property
    def total_price(self):
        """Общая стоимость данного элемента (цена за единицу * количество)"""
        return self.product_variant.price * self.quantity
