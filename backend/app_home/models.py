from django.db import models


class Slider(models.Model):
    image = models.ImageField(upload_to='slider_images/', verbose_name='Изображение')
    alt_text = models.CharField(max_length=200, verbose_name='Описание изображения (alt текст)')
    is_active = models.BooleanField(default=True, verbose_name='Отображать')

    class Meta:
        verbose_name = 'Слайдер'
        verbose_name_plural = 'Слайдеры'
        ordering = ['-id']

    def __str__(self):
        return f'Слайд {self.id} - {self.alt_text}'


class CompanyDetails(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name = 'Реквизиты компании'
        verbose_name_plural = 'Реквизиты компании'
        ordering = ['name']

    def __str__(self):
        return self.name


class SiteLogo(models.Model):
    logo = models.ImageField(upload_to='logo/', verbose_name='Логотип', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Логотип сайта'
        verbose_name_plural = 'Логотип сайта'
        # Ограничение, чтобы была только одна запись
        # Это достигается с помощью бизнес-логики в представлении

    def __str__(self):
        return f"Логотип сайта ({'установлен' if self.logo else 'не установлен'})"

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SocialNetwork(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    icon = models.ImageField(upload_to='social_icons/', verbose_name='Иконка')
    link = models.URLField(verbose_name='Ссылка')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Социальные сети'
        ordering = ['name']

    def __str__(self):
        return self.name
