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


class Size(models.Model):
    name = models.CharField(max_length=100, verbose_name='Размер')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Размер'
        verbose_name_plural = 'Размеры'
        ordering = ['name']

    def __str__(self):
        return self.name


class Fabric(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ткань')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Ткань'
        verbose_name_plural = 'Ткани'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, verbose_name='Подкатегория')
    name = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    binding = models.TextField(blank=True, null=True, verbose_name='Переплет')
    picture_title = models.TextField(blank=True, null=True, verbose_name='Название рисунка')
    fabric_type = models.ForeignKey(Fabric, on_delete=models.SET_NULL, verbose_name='Тип ткани', blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_promotion = models.BooleanField(default=False, verbose_name='Акция')
    is_new = models.BooleanField(default=False, verbose_name='Новинка')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['name']

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name='Товар')
    image = models.ImageField(upload_to='product_images/', verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Фотография товара'
        verbose_name_plural = 'Фотографии товаров'
        ordering = ['-created_at']

    def __str__(self):
        return f"Фото для {self.product.name}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants', verbose_name='Товар')
    size = models.ForeignKey(Size, on_delete=models.CASCADE, verbose_name='Размер')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    is_active = models.BooleanField(default=True, verbose_name='Активен')

    class Meta:
        verbose_name = 'Вариант товара'
        verbose_name_plural = 'Варианты товаров'
        ordering = ['product', 'size']

    def __str__(self):
        return f"{self.product.name} - {self.size.name} - {self.price}"


class Store(models.Model):
    city = models.CharField(max_length=100, verbose_name='Город')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True, null=True)
    work_schedule = models.TextField(verbose_name='График работы')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'
        ordering = ['city', 'address']

    def __str__(self):
        return f'{self.city}, {self.address}'
