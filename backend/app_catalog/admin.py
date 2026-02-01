from django.contrib import admin
from .models import Category, Subcategory, Size, Fabric, Product, ProductVariant, Store

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

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory', 'fabric_type', 'is_active', 'is_promotion', 'is_new')
    list_filter = ('is_active', 'is_promotion', 'is_new', 'category', 'subcategory', 'fabric_type')
    search_fields = ('name', 'description')
    ordering = ('name',)

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'price', 'is_active')
    list_filter = ('is_active', 'product', 'size')
    search_fields = ('product__name', 'size__name')
    ordering = ('product', 'size')

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('city', 'address', 'work_schedule')
    list_filter = ('city',)
    search_fields = ('city', 'address')
    ordering = ('city', 'address')
