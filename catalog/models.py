from django.db import models
from django.urls import reverse


NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='categories/', verbose_name='Изображение')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=250, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='goods/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    # manufactured_at = models.DateField(default=timezone.now, verbose_name='Дата производства продукта')

    def __str__(self):
        return f'{self.name} [{self.category.name}] {self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class BlogPost(models.Model):
    objects = models.Manager()

    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.CharField(max_length=150, null=True, blank=True, verbose_name='slug')
    content = models.TextField(verbose_name='Содержание')
    preview = models.ImageField(upload_to='blog_previews/', blank=True, null=True, verbose_name='Превью')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    published = models.BooleanField(default=False, verbose_name='Опубликовано')
    view_count = models.PositiveIntegerField(default=0, verbose_name='Количеств просмотров')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Блог пост'
        verbose_name_plural = 'Блог посты'

    def __str__(self):
        return f'{self.title}'

    def get_absolute_url(self):
        return reverse('catalog:blogpost_detail', kwargs={'slug': self.slug})


class Version(models.Model):
    objects = models.Manager()

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    version_number = models.CharField(max_length=10, verbose_name='Номер версии')
    version_name = models.CharField(max_length=100, verbose_name='Название версии')
    is_current = models.BooleanField(default=False, verbose_name='Текущая версия')

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'

    def __str__(self):
        return f'{self.product} {self.version_number} {self.version_name} {self.is_current}'

