from django.urls import path
from . import views

urlpatterns = [
    # Category endpoints
    path('categories/', views.CategoryListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),

    # Subcategory endpoints
    path('subcategories/', views.SubcategoryListCreateView.as_view(), name='subcategory-list-create'),
    path('subcategories/<int:pk>/', views.SubcategoryDetailView.as_view(), name='subcategory-detail'),

    # Size endpoints
    path('sizes/', views.SizeListCreateView.as_view(), name='size-list-create'),
    path('sizes/<int:pk>/', views.SizeDetailView.as_view(), name='size-detail'),

    # Fabric endpoints
    path('fabrics/', views.FabricListCreateView.as_view(), name='fabric-list-create'),
    path('fabrics/<int:pk>/', views.FabricDetailView.as_view(), name='fabric-detail'),

    # Product endpoints (with variants included in detail view)
    path('products/', views.ProductListCreateView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'),

    # Product with variants list endpoint
    path('products-with-variants/', views.ProductWithVariantsListView.as_view(), name='product-with-variants-list'),
]