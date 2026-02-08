from django.contrib import admin
from .models import Category, Subcategory, Size, Fabric, Product, ProductVariant, ProductImage


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
    fields = ('size', 'price', 'is_active')
    verbose_name = 'Вариант товара'
    verbose_name_plural = 'Варианты товаров'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin interface for Product model with inline variants and images.
    """
    list_display = ('name', 'category', 'subcategory', 'is_active', 'is_promotion', 'is_new')
    list_filter = ('category', 'subcategory', 'is_active', 'is_promotion', 'is_new', 'fabric_type')
    search_fields = ('name', 'description')
    # fabric_type is a ForeignKey, not a many-to-many field, so no filter_horizontal needed
    inlines = [ProductImageInline, ProductVariantInline]  # Include the images and variants inline
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'subcategory', 'name', 'description', 'binding', 'picture_title', 'fabric_type')
        }),
        ('Статус', {
            'fields': ('is_active', 'is_promotion', 'is_new'),
            'classes': ('collapse',)
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Customize the queryset for foreign key fields.
        """
        if db_field.name == "fabric_type":
            kwargs["queryset"] = Fabric.objects.filter(is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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


