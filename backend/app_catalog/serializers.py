from rest_framework import serializers
from .models import Category, Subcategory, Size, Fabric, Product, ProductVariant


class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Size
        fields = '__all__'


class FabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabric
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductVariantSerializer(serializers.ModelSerializer):
    size = SizeSerializer(read_only=True)
    
    class Meta:
        model = ProductVariant
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)
    fabric_type = FabricSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = '__all__'


class ProductListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubcategorySerializer(read_only=True)
    fabric_type = FabricSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'subcategory', 'fabric_type', 'binding', 'picture_title', 'image', 'is_active', 'is_promotion', 'is_new']