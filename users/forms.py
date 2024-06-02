from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class CustomAuthenticationForm(AuthenticationForm):
    # Здесь вы можете добавить дополнительную логику или поля
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Например, изменить атрибуты поля
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
