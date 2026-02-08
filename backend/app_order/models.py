from django.db import models
from django.conf import settings
from app_home.models import DeliveryOption
from app_catalog.models import ProductVariant


class Order(models.Model):
    """
    Модель заказа
    """
    STATUS_CHOICES = [
        ('pending', 'В ожидании'),
        ('confirmed', 'Подтвержден'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь', null=True, blank=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.TextField(verbose_name='Адрес доставки')
    delivery_option = models.ForeignKey(DeliveryOption, on_delete=models.SET_NULL, null=True, verbose_name='Вариант доставки')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая сумма')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус заказа')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_at']

    def __str__(self):
        return f'Заказ #{self.id} - {self.first_name} {self.last_name}'


class OrderItem(models.Model):
    """
    Элемент заказа - связывает заказ, товарный вариант и количество
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items', verbose_name='Заказ')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, verbose_name='Вариант товара')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу', default=0)

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.quantity}x {self.product_variant.product.name} ({self.product_variant.size.name})'

    @property
    def total_price(self):
        """Общая стоимость данного элемента (цена за единицу * количество)"""
        if self.price is not None:
            return self.price * self.quantity
        return 0
