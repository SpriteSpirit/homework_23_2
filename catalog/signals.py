from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import BlogPost


# Сигнал, который отправляет письмо, если статья достигла 100 просмотров.
@receiver(post_save, sender=BlogPost)
def send_congratulations_email(instance, **kwargs):
    congrats_count = 100

    if instance.view_count == congrats_count:
        url = instance.get_absolute_url()
        send_mail(
            'Поздравляем с достижением!',
            f'Ваша статья "{instance.title}" достигла {congrats_count} просмотров!'
            f'Вы можете просмотреть ее по ссылке: {url}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
