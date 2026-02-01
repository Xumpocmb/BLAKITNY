from django.contrib import admin
from .models import Category, Subcategory, Store

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_active')
    list_filter = ('is_active', 'category')
    search_fields = ('name', 'description', 'category__name')
    ordering = ('category', 'name')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'work_schedule')
    list_filter = ('city',)
    search_fields = ('city', 'address')
    ordering = ('city', 'address')
