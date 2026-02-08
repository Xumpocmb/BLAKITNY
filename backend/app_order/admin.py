from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone", "delivery_option", "total_amount", "status", "created_at")
    list_filter = ("status", "created_at", "delivery_option")
    search_fields = ("first_name", "last_name", "email", "phone", "address")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
    list_display_links = ("id", "first_name", "last_name")
