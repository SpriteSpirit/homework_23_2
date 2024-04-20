from django.urls import path
from .views import home, categories, contacts, get_product_detail
from .views import create_product, get_product_list

app_name = 'catalog'

urlpatterns = [
    path('', home, name='home'),
    path('categories/', categories, name='categories'),
    path('contacts/', contacts, name='contacts'),
    path('<int:pk>/product/', get_product_detail, name='product_detail'),
    path('create/product/', create_product, name='create_product'),
    path('products/', get_product_list, name='product_list'),
]
