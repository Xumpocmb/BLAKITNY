from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Профиль пользователя, расширяющий встроенную модель User
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    is_archived = models.BooleanField(default=False, verbose_name='Архивирован')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'Профиль {self.user.username}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создает профиль пользователя автоматически при создании пользователя"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль пользователя при сохранении пользователя"""
    # Проверяем, существует ли профиль и не находится ли он в процессе сохранения
    try:
        profile = instance.profile
        # Не вызываем сохранение профиля здесь, чтобы избежать рекурсии
        # Профиль сохраняется отдельно при необходимости
    except UserProfile.DoesNotExist:
        # Если профиля нет, создаем его
        UserProfile.objects.create(user=instance)
