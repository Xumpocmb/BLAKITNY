from django.contrib import admin
from .models import Slider, CompanyDetails


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
