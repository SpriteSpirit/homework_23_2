from django.urls import path
from .views import HomeView, CategoryListView, ContactsView, ProductDetailView
from .views import CreateProductView, ProductListView

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product_detail'),
    path('create/product/', CreateProductView.as_view(), name='create_product'),
    path('products/', ProductListView.as_view(), name='product_list'),
]
