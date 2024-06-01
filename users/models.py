from django.contrib.auth.models import AbstractUser
from django.db import models
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

from catalog.models import NULLABLE


# Create your models here.
class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='email')
    phone = PhoneNumberField(blank=True, null=True, verbose_name='phone', help_text='Введите номер телефона')
    tg_name = models.CharField(max_length=50, verbose_name='Ник Telegram', help_text='Введите свой ник', **NULLABLE)
    avatar = models.ImageField(upload_to='users/avatars/',  **NULLABLE)
    country = CountryField(blank_label="(select country)", verbose_name='Страна')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email
