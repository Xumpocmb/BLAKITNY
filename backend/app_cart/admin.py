from django.contrib import admin
from .models import Cart, CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_items', 'total_price', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product_variant', 'quantity', 'get_total_price')
    list_filter = ('cart__user',)
    raw_id_fields = ('cart', 'product_variant')
    
    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = 'Общая цена'
