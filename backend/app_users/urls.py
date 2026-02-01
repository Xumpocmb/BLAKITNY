from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('refresh/', views.refresh_view, name='token-refresh'),
    path('me/', views.me_view, name='user-me'),
]
