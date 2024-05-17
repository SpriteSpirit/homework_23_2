from django.urls import path
from .views import HomeView, CategoryListView, ContactsView, ProductDetailView
from .views import create_product, get_product_list

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product_detail'),
    path('create/product/', create_product, name='create_product'),
    path('products/', get_product_list, name='product_list'),
]
