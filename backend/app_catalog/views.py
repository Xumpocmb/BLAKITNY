from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Category, Subcategory, Size, Fabric, Product, Store
from .serializers import (
    CategorySerializer, SubcategorySerializer,
    SizeSerializer, FabricSerializer,
    ProductSerializer, ProductListSerializer, StoreSerializer
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


class ProductListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer  # Use simplified serializer for list view


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # Use detailed serializer for detail view


class ProductWithVariantsListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.prefetch_related('variants', 'images', 'category', 'subcategory', 'fabric_type').filter(is_active=True)
    serializer_class = ProductSerializer  # Use detailed serializer that includes variants


class StoreListCreateView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer