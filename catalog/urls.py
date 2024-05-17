from django.urls import path
from .views import HomeView, CategoryListView, ContactsView, ProductDetailView, BlogPostListView, BlogPostDetailView, \
    BlogPostCreateView, BlogPostUpdateView, BlogPostDeleteView
from .views import CreateProductView, ProductListView

app_name = 'catalog'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('<int:pk>/product/', ProductDetailView.as_view(), name='product_detail'),
    path('create/product/', CreateProductView.as_view(), name='create_product'),
    path('products/', ProductListView.as_view(), name='product_list'),

    path('blogpost/', BlogPostListView.as_view(), name='blogpost_list'),
    path('<slug:slug>/view/', BlogPostDetailView.as_view(), name='blogpost_detail'),
    path('create/', BlogPostCreateView.as_view(), name='blogpost_create'),
    path('<slug:slug>/update/', BlogPostUpdateView.as_view(), name='blogpost_update'),
    path('<slug:slug>/delete/', BlogPostDeleteView.as_view(), name='blogpost_confirm_delete'),
]
