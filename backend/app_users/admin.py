from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileInline(admin.StackedInline):
    """
    Инлайн-редактор для профиля пользователя
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Профили пользователей'
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    """
    Расширенный административный интерфейс для пользователя
    """
    inlines = (UserProfileInline,)

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)


# Переопределяем стандартный UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
