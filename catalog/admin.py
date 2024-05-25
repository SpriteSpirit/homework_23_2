from django.contrib import admin
from catalog.models import Category, Product, BlogPost, Version


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'created_at', 'updated_at']
    list_filter = ['category']
    search_fields = ['name', 'description']


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'content', 'preview', 'published', 'view_count', 'created_at']
    list_filter = ['title', 'created_at']
    search_fields = ['title', 'content']


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ['product', 'version_number', 'version_name', 'is_current']
    list_filter = ['version_number']
    search_fields = ['product', 'version_number']
