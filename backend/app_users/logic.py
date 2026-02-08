"""
Модуль содержит бизнес-логику для работы с пользователями.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import transaction
from .models import UserProfile

User = get_user_model()


def change_password(user, old_password, new_password, confirm_new_password):
    """
    Изменяет пароль пользователя.
    
    Args:
        user: Объект пользователя
        old_password: Старый пароль
        new_password: Новый пароль
        confirm_new_password: Подтверждение нового пароля
    
    Returns:
        bool: True, если пароль успешно изменен, иначе False
    """
    # Проверяем, совпадает ли старый пароль
    if not user.check_password(old_password):
        return False
    
    # Проверяем, совпадают ли новые пароли
    if new_password != confirm_new_password:
        return False
    
    # Проверяем минимальную длину пароля
    if len(new_password) < 8:
        return False
    
    # Устанавливаем новый пароль
    user.password = make_password(new_password)
    user.save(update_fields=['password'])
    return True


def change_email(user, new_email):
    """
    Изменяет email пользователя.
    
    Args:
        user: Объект пользователя
        new_email: Новый email
    
    Returns:
        bool: True, если email успешно изменен, иначе False
    """
    # Проверяем валидность email
    try:
        validate_email(new_email)
    except ValidationError:
        return False
    
    # Проверяем, не занят ли уже этот email
    if User.objects.filter(email=new_email).exclude(id=user.id).exists():
        return False
    
    # Обновляем email
    user.email = new_email
    user.save(update_fields=['email'])
    return True


def archive_user(user):
    """
    Архивирует профиль пользователя (на самом деле не удаляет, а помечает как архивный).
    
    Args:
        user: Объект пользователя
    
    Returns:
        bool: True, если пользователь успешно архивирован, иначе False
    """
    try:
        profile = user.profile
        if profile.is_archived:
            return False  # Пользователь уже архивирован
        
        profile.archive()
        return True
    except UserProfile.DoesNotExist:
        # Создаем профиль, если его нет, и затем архивируем
        profile = UserProfile.objects.create(user=user)
        profile.archive()
        return True


def restore_user(user):
    """
    Восстанавливает профиль пользователя из архива.
    
    Args:
        user: Объект пользователя
    
    Returns:
        bool: True, если пользователь успешно восстановлен, иначе False
    """
    try:
        profile = user.profile
        if not profile.is_archived:
            return False  # Пользователь не архивирован
        
        profile.restore()
        return True
    except UserProfile.DoesNotExist:
        return False  # Профиль не существует


def update_avatar(user, avatar_file):
    """
    Обновляет аватар пользователя.
    
    Args:
        user: Объект пользователя
        avatar_file: Файл аватара
    
    Returns:
        bool: True, если аватар успешно обновлен, иначе False
    """
    try:
        profile, created = UserProfile.objects.get_or_create(user=user)
        profile.avatar = avatar_file
        profile.save(update_fields=['avatar'])
        return True
    except Exception:
        return False


def get_user_profile(user_id):
    """
    Возвращает профиль пользователя по ID.
    
    Args:
        user_id: ID пользователя
    
    Returns:
        User: Объект пользователя или None, если не найден
    """
    try:
        user = User.objects.get(id=user_id)
        # Проверяем, не архивирован ли пользователь
        if hasattr(user, 'profile') and user.profile.is_archived:
            return None
        return user
    except User.DoesNotExist:
        return None