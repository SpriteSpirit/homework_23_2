from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from users.apps import UsersConfig
from users.views import UserCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', UserCreateView.as_view(), name='register'),
    # path('profile/', 'users.views.profile', name='profile'),
    # path('profile/edit/', 'users.views.edit_profile', name='edit_profile'),
    # path('profile/password/', 'users.views.change_password', name='change_password'),
    # path('profile/delete/', 'users.views.delete_profile', name='delete_profile'),
    # path('profile/orders/', 'users.views.orders', name='orders'),
    # path('profile/orders/<int:pk>/', 'users.views.order_detail', name='order_detail'),
]
