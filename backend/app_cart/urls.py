from django.urls import path
from . import views

urlpatterns = [
    # Cart endpoints
    path('', views.CartDetailView.as_view(), name='cart-detail'),
    path('add/', views.add_to_cart, name='cart-add'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='cart-remove'),
    path('update/<int:item_id>/', views.update_cart_item, name='cart-update'),
    path('clear/', views.clear_cart, name='cart-clear'),
]