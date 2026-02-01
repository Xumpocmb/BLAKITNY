from django.contrib import admin
from .models import Category, Subcategory, FilterType, FilterParameter, Store

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

@admin.register(FilterType)
class FilterTypeAdmin(admin.ModelAdmin):
    list_display = ('filter_type', 'is_active')
    list_filter = ('is_active', 'filter_type')
    search_fields = ('filter_type',)
    ordering = ('filter_type',)

@admin.register(FilterParameter)
class FilterParameterAdmin(admin.ModelAdmin):
    list_display = ('parameter', 'filter_type', 'is_active')
    list_filter = ('is_active', 'filter_type')
    search_fields = ('parameter', 'filter_type__filter_type')
    ordering = ('filter_type', 'parameter')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'work_schedule')
    list_filter = ('city',)
    search_fields = ('city', 'address')
    ordering = ('city', 'address')
