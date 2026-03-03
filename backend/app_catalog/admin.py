from django.contrib import admin
from .models import Category, Subcategory, Size, Fabric, PictureTitle, Product, ProductVariant, ProductImage


class ProductImageInline(admin.TabularInline):
    """
    Inline admin for ProductImage model to manage images directly from Product admin.
    """
    model = ProductImage
    extra = 1  # Number of empty forms to display
    fields = ('image', 'is_active')
    verbose_name = 'Фотография товара'
    verbose_name_plural = 'Фотографии товаров'


class ProductVariantInline(admin.TabularInline):
    """
    Inline admin for ProductVariant model to manage variants directly from Product admin.
    """
    model = ProductVariant
    extra = 1  # Number of empty forms to display
    fields = ('size', 'fabric', 'picture_title', 'price', 'is_active')
    verbose_name = 'Вариант товара'
    verbose_name_plural = 'Варианты товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product model with inline variants and images.
    """
    list_display = ('name', 'category', 'subcategory', 'is_active', 'is_promotion', 'is_new')
    list_filter = ('category', 'subcategory', 'is_active', 'is_promotion', 'is_new')
    search_fields = ('name', 'description')
    inlines = [ProductImageInline, ProductVariantInline]  # Include the images and variants inline
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'subcategory', 'name', 'description', 'binding')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_promotion', 'is_new'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Category model.
    """
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for Subcategory model.
    """
    list_display = ('name', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'description')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    """
    Admin interface for Size model.
    """
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Fabric)
class FabricAdmin(admin.ModelAdmin):
    """
    Admin interface for Fabric model.
    """
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(PictureTitle)
class PictureTitleAdmin(admin.ModelAdmin):
    """
    Admin interface for PictureTitle model.
    """
    list_display = ('name', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)


