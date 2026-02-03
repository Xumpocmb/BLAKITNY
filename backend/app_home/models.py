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
