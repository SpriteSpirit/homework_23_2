from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from catalog.forms import StyleFormMixin
from users.models import User
from django.utils.translation import gettext_lazy as _


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']  # Поля, которые можно редактировать
        labels = {
            'email': _('Email'),
            'first_name': _('First Name'),
            'last_name': _('Last Name'),
        }


class CustomAuthenticationForm(AuthenticationForm):
    # Здесь вы можете добавить дополнительную логику или поля
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Например, изменить атрибуты поля
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
