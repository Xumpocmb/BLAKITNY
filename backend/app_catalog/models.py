from django.db import models


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
