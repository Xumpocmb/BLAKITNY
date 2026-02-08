from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """
    Встроенный интерфейс для редактирования элементов заказа
    """
    model = OrderItem
    extra = 1
    readonly_fields = ('total_price',)
    
    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        # Ограничиваем выбор вариантов продукта только активными
        if hasattr(formset.form.base_fields['product_variant'], 'queryset'):
            formset.form.base_fields['product_variant'].queryset = formset.form.base_fields['product_variant'].queryset.filter(is_active=True)
        return formset


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id", 
        "first_name", 
        "last_name", 
        "email", 
        "phone", 
        "delivery_option", 
        "total_amount", 
        "status", 
        "created_at",
        "order_summary"
    )
    list_filter = ("status", "created_at", "delivery_option", "user")
    search_fields = ("first_name", "last_name", "email", "phone", "address", "user__username", "id")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
    list_display_links = ("id", "first_name", "last_name")
    
    # Добавляем фильтрацию по дате
    date_hierarchy = 'created_at'
    
    # Встраиваем элементы заказа
    inlines = [OrderItemInline]
    
    # Настройка отображения деталей заказа
    fieldsets = (
        ("Информация о клиенте", {
            'fields': ('user', 'first_name', 'last_name', 'email', 'phone')
        }),
        ("Адрес и доставка", {
            'fields': ('address', 'delivery_option')
        }),
        ("Информация о заказе", {
            'fields': ('total_amount', 'status', 'created_at', 'updated_at')
        }),
    )
    
    def order_summary(self, obj):
        """Отображает краткое описание заказа в списке"""
        if obj.order_items.exists():
            items_count = obj.order_items.count()
            items_names = ", ".join([item.product_variant.product.name[:30] for item in obj.order_items.all()[:3]])
            if obj.order_items.count() > 3:
                items_names += "..."
            return f"{items_count} товар(ов): {items_names}"
        return "Нет товаров"
    order_summary.short_description = "Содержимое заказа"


@admin.register(Order)
class OrderAdminWrapper(OrderAdmin):
    pass


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_variant', 'quantity', 'price', 'total_price')
    list_filter = ('order__status', 'product_variant__product__name', 'order__created_at')
    search_fields = ('order__id', 'product_variant__product__name', 'order__first_name', 'order__last_name')
    readonly_fields = ('total_price',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('order', 'product_variant__product', 'product_variant__size')
