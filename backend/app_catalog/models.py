from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='category_images/', blank=True, null=True, verbose_name='Картинка')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')
    is_active = models.BooleanField(default=True, verbose_name='Активна')

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ['name']

    def __str__(self):
        return self.name


class FilterType(models.Model):
    filter_type = models.CharField(max_length=50, verbose_name='Тип фильтра')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Тип фильтра'
        verbose_name_plural = 'Типы фильтров'
        ordering = ['filter_type']

    def __str__(self):
        return self.filter_type


class FilterParameter(models.Model):
    filter_type = models.ForeignKey(FilterType, on_delete=models.CASCADE, related_name='filter_parameters', verbose_name='Тип фильтра')
    parameter = models.CharField(max_length=100, verbose_name='Параметр')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Параметр фильтра'
        verbose_name_plural = 'Параметры фильтров'
        ordering = ['filter_type', 'parameter']

    def __str__(self):
        return f"{self.filter_type.filter_type}: {self.parameter}"


class Store(models.Model):
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    work_schedule = models.TextField(verbose_name='График работы')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['city', 'address']

    def __str__(self):
        return f'{self.city}, {self.address}'
