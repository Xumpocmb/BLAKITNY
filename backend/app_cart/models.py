from django.db import models
from django.contrib.auth.models import User
from app_catalog.models import ProductVariant


class Cart(models.Model):
    """
    Модель корзины покупок пользователя
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина {self.user.username}'

    @property
    def total_price(self):
        """Общая стоимость всех товаров в корзине"""
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        """Общее количество товаров в корзине"""
        return sum(item.quantity for item in self.items.all())


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
