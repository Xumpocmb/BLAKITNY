from django.contrib import admin
from .models import Slider, CompanyDetails, SiteLogo, SocialNetwork, DeliveryPayment


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ("id", "image", "alt_text", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("alt_text",)
    list_display_links = ("id", "image")


@admin.register(CompanyDetails)
class CompanyDetailsAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name", "description")
    list_display_links = ("id", "name")


@admin.register(SiteLogo)
class SiteLogoAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        # Запрещаем добавление новых записей, если уже существует
        count = SiteLogo.objects.count()
        if count > 0:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Разрешаем удаление только если есть более одной записи (хотя по логике не должно быть)
        return SiteLogo.objects.count() > 1


@admin.register(SocialNetwork)
class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "link", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name", "link")
    list_display_links = ("id", "name")


@admin.register(DeliveryPayment)
class DeliveryPaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "__str__", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        # Запрещаем добавление новых записей, если уже существует
        count = DeliveryPayment.objects.count()
        if count > 0:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление единственной записи
        return False
