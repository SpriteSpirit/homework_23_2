from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView, LoginView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import CreateView

from users.forms import UserRegisterForm, CustomAuthenticationForm
from users.models import User

from random import randint

from config.settings import EMAIL_HOST_USER

import secrets
from django.utils.html import strip_tags


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()

        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}/'

        send_mail(
            subject='Подтверждение почты',
            message=f'Чтобы подтвердить вашу почту - перейдите по ссылке:  {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )

        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    html_email_template_name = None
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = User.objects.get(email=email)
        new_password = generate_password()
        user.set_password(new_password)
        user.save()

        # Token generation for password reset
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Prepare email content
        subject = 'Восстановление и сброс пароля'
        reset_link = self.request.build_absolute_uri(reverse_lazy('users:password_reset_confirm', args=[uid, token]))

        html_message = render_to_string('users/password_reset_email.html', {
            'user': user,
            'uid': uid,
            'token': token,
            'site_name': 'KUKUSHKA',
            'password': new_password,
            'reset_link': reset_link,
        })

        plain_message = strip_tags(html_message)
        send_mail(subject, plain_message, from_email=EMAIL_HOST_USER, recipient_list=[user.email],
                  html_message=html_message)

        return redirect(reverse('users:password_reset_done'))


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'


def generate_password():
    password = ''
    chars = '+-/*!&$#?=@<>abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

    for i in range(randint(8, 12)):
        password += secrets.choice(chars)

    return password
