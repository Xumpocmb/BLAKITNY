from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Category, Subcategory, Size, Fabric, Product
from .serializers import (
    CategorySerializer, SubcategorySerializer,
    SizeSerializer, FabricSerializer,
    ProductSerializer
)


class CategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class SubcategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class SizeListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class SizeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class FabricListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer


class FabricDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer


class ProductListView(generics.ListAPIView):
    """
    Возвращает список товаров.

    Опционально поддерживает фильтрацию по категории через query-параметр.
    Каждый товар включает в себя варианты (variants), изображения, категорию, подкатегорию и тип ткани.

    Query Parameters:
        category_id (int, optional): ID категории для фильтрации товаров

    Returns:
        list: Список товаров с вариантами и изображениями

    Example:
        GET /api/catalog/products/ — все товары
        GET /api/catalog/products/?category_id=1 — товары категории 1
    """
    permission_classes = [AllowAny]
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.prefetch_related('variants', 'images', 'category', 'subcategory', 'fabric_type')
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Возвращает, обновляет или удаляет конкретный товар.

    Возвращает полную информацию о товаре, включая варианты (variants), изображения,
    категорию, подкатегорию и тип ткани.

    Returns:
        object: Объект товара с вариантами и изображениями

    Example:
        GET /api/catalog/products/1/ — получить товар с ID=1
        PUT /api/catalog/products/1/ — обновить товар с ID=1
        DELETE /api/catalog/products/1/ — удалить товар с ID=1
    """
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class SubcategoryByCategoryView(generics.ListAPIView):
    """
    Возвращает все подкатегории для указанной категории.
    """
    permission_classes = [AllowAny]
    serializer_class = SubcategorySerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Subcategory.objects.filter(category_id=category_id, is_active=True)


