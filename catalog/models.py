from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.CharField(max_length=1000, verbose_name='Описание')
    image = models.ImageField(upload_to='goods/', verbose_name='Изображение')
    category = models.CharField(max_length=100, verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена')
    data_create = models.DateTimeField(verbose_name='Дата создания')
    data_changed = models.DateTimeField(verbose_name='Дата изменения')

    def __str__(self):
        return f'{self.name}\n{self.description}\n{self.category}\n{self.price}\n{self.data_create}\n{self.data_changed}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
