from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Product(models.Model):
    name = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Название')
    description = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='Описание')
    image = models.ImageField(upload_to='goods/', verbose_name='Изображение')
    category = models.CharField(max_length=100, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    data_create = models.DateTimeField(verbose_name='Дата создания')
    data_changed = models.DateTimeField(verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.name}\n{self.category}\n{self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
