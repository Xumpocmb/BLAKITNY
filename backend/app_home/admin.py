from django.contrib import admin
from .models import Slider, CompanyDetails, SiteLogo, SocialNetwork, DeliveryPayment, AboutUs, Feedback, DeliveryOption


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


@admin.register(DeliveryOption)
class DeliveryOptionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("name",)
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


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    def has_add_permission(self, request):
        # Запрещаем добавление новых записей, если уже существует
        count = AboutUs.objects.count()
        if count > 0:
            return False
        return True

    def has_delete_permission(self, request, obj=None):
        # Запрещаем удаление единственной записи
        return False


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "phone", "created_at", "short_message")
    list_filter = ("created_at",)
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at",)
    list_display_links = ("id", "name")

    def short_message(self, obj):
        """Display a shortened version of the message in the admin list view"""
        return obj.message[:50] + "..." if len(obj.message) > 50 else obj.message
    short_message.short_description = "Сообщение"
