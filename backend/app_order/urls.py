from django.urls import path
from . import views

urlpatterns = [
    path('', views.OrderListView.as_view(), name='order-list'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('create/', views.create_order, name='order-create'),
    path('<int:pk>/update-status/', views.update_order_status_view, name='order-update-status'),
    path('<int:pk>/cancel/', views.cancel_order_view, name='order-cancel'),
    path('stats/', views.get_order_stats, name='order-stats'),
]