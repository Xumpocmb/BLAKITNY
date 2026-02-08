from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('refresh/', views.refresh_view, name='refresh'),
    path('me/', views.me_view, name='me'),
    path('profile/', views.get_profile, name='get_profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('change-email/', views.change_email_view, name='change_email'),
    path('update-avatar/', views.update_avatar, name='update_avatar'),
    path('archive-account/', views.archive_account, name='archive_account'),
    path('delete-account/', views.delete_account, name='delete_account'),
]
