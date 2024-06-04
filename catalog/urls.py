from django.urls import path
from django.views.decorators.cache import cache_page

from .views import HomeView, CategoryListView, ContactsView, ProductDetailView, BlogPostListView, BlogPostDetailView, \
    BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView, ProductUpdateView, ProductDeleteView
from .views import ProductCreateView, ProductListView

app_name = 'catalog'

timeout30min = 60*30
timeout20min = 60*20
timeout10min = 60*10

urlpatterns = [
    path('', cache_page(timeout20min)(HomeView.as_view()), name='home'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('<int:pk>/product/', cache_page(timeout10min)(ProductDetailView.as_view()), name='product_detail'),
    path('create/product/', ProductCreateView.as_view(), name='create_product'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='update_product'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_confirm_delete'),
    path('products/', ProductListView.as_view(), name='product_list'),

    path('blogpost/', cache_page(timeout30min)(BlogPostListView.as_view()), name='blogpost_list'),
    path('<slug:slug>/view/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('<slug:slug>/update/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='blogpost_confirm_delete'),
]
