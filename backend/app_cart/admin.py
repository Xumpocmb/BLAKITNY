from django.contrib import admin
from django.utils.html import format_html
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ('get_product_name', 'get_product_size', 'get_product_price', 'get_total_price')
    fields = ('product_variant', 'get_product_name', 'get_product_size', 'get_product_price', 'quantity', 'get_total_price')
    
    def get_product_name(self, obj):
        if obj.product_variant and obj.product_variant.product:
            return obj.product_variant.product.name
        return '-'
    get_product_name.short_description = 'Название товара'
    
    def get_product_size(self, obj):
        if obj.product_variant and obj.product_variant.size:
            return obj.product_variant.size.name
        return '-'
    get_product_size.short_description = 'Размер'
    
    def get_product_price(self, obj):
        if obj.product_variant:
            return f"{obj.product_variant.price} руб."
        return '-'
    get_product_price.short_description = 'Цена за ед.'
    
    def get_total_price(self, obj):
        if obj.pk:  # Only calculate if object exists (has been saved)
            return f"{obj.total_price} руб."
        return '-'
    get_total_price.short_description = 'Общая цена'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_username', 'total_items', 'total_price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'total_items_display', 'total_price_display')
    inlines = [CartItemInline]
    
    def display_username(self, obj):
        """Display full name if available, otherwise username"""
        user = obj.user
        full_name = user.get_full_name().strip()
        if full_name:
            return full_name
        return user.username
    display_username.short_description = 'Имя пользователя'
    display_username.admin_order_field = 'user__first_name'
    
    def total_items_display(self, obj):
        """Display total items in the cart"""
        return obj.total_items
    total_items_display.short_description = 'Всего товаров в корзине'
    
    def total_price_display(self, obj):
        """Display total price of the cart"""
        return f"{obj.total_price} руб."
    total_price_display.short_description = 'Общая стоимость корзины'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'display_cart_user', 'product_name', 'product_size', 'quantity', 'unit_price', 'get_total_price')
    list_filter = ('cart__user', 'product_variant__product__name', 'product_variant__size__name', 'cart__created_at')
    search_fields = ('cart__user__username', 'cart__user__email', 'product_variant__product__name')
    raw_id_fields = ('cart', 'product_variant')
    readonly_fields = ('get_total_price',)
    
    def display_cart_user(self, obj):
        """Display the user associated with the cart"""
        return obj.cart.user.username
    display_cart_user.short_description = 'Пользователь'
    display_cart_user.admin_order_field = 'cart__user__username'
    
    def product_name(self, obj):
        """Display the product name"""
        if obj.product_variant and obj.product_variant.product:
            return obj.product_variant.product.name
        return '-'
    product_name.short_description = 'Товар'
    product_name.admin_order_field = 'product_variant__product__name'
    
    def product_size(self, obj):
        """Display the product size"""
        if obj.product_variant and obj.product_variant.size:
            return obj.product_variant.size.name
        return '-'
    product_size.short_description = 'Размер'
    product_size.admin_order_field = 'product_variant__size__name'
    
    def unit_price(self, obj):
        """Display the unit price of the product variant"""
        if obj.product_variant:
            return f"{obj.product_variant.price} руб."
        return '-'
    unit_price.short_description = 'Цена за ед.'
    
    def get_total_price(self, obj):
        """Display the total price for this cart item"""
        return f"{obj.total_price} руб."
    get_total_price.short_description = 'Общая цена'
