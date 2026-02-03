from rest_framework import generics
from rest_framework.response import Response
from .models import Category, Subcategory, Size, Fabric, Product
from .serializers import (
    CategorySerializer, SubcategorySerializer,
    SizeSerializer, FabricSerializer,
    ProductSerializer, ProductListSerializer
)


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryListCreateView(generics.ListCreateAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class SubcategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class SizeListCreateView(generics.ListCreateAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class SizeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Size.objects.all()
    serializer_class = SizeSerializer


class FabricListCreateView(generics.ListCreateAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer


class FabricDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Fabric.objects.all()
    serializer_class = FabricSerializer


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer  # Use simplified serializer for list view


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # Use detailed serializer for detail view


class ProductWithVariantsListView(generics.ListAPIView):
    queryset = Product.objects.prefetch_related('variants', 'images', 'category', 'subcategory', 'fabric_type').filter(is_active=True)
    serializer_class = ProductSerializer  # Use detailed serializer that includes variants