from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages
from .utils import slugify

from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm
from .models import Product, Category, BlogPost


class HomeView(TemplateView):
    template_name = 'catalog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = Product.objects.order_by('-price')[:3]
        context['title'] = 'KUKUSHKA STORE'

        return context

    def post(self, request, *args, **kwargs):
        search = request.POST.get('search')
        print(f'Search: {search}')

        return self.get(request, *args, **kwargs)


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'КОНТАКТЫ'
        context['address'] = 'г. Санкт-Петербург,\n м. Сенная площадь,\n ул. Садовая, 54'
        context['phone'] = '+7 (812) 123-45-67'
        context['social'] = 'Telegram: @kukushka_store'

        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        search = request.POST.get('search')

        if search is not None:
            print(f'Search: {search}')
        else:
            print(f'Имя: {name}\nЭл.Почта: {email}\nТелефон:{phone}')

        return self.get(request, *args, **kwargs)


class CategoryListView(ListView):
    model = Category
    context_object_name = 'object_list'
    template_name = 'catalog/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'КАТАЛОГ'
        return context

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'object'
    template_name = 'catalog/product_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        return context

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)

        return get_object_or_404(Product, id=pk)


class CreateProductView(CreateView):
    model = Product
    form_class = ProductForm

    def form_valid(self, form):
        product = form.save(commit=False)
        product.save()
        messages.success(self.request, 'Товар успешно создан')
        return redirect('catalog:product_list')

    def get_success_url(self):
        return reverse_lazy('catalog:product_list')


class ProductListView(ListView):
    model = Product
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'СПИСОК ТОВАРОВ'
        return context


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'blogposts'

    # paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        queryset = queryset.order_by('created_at')

        return queryset


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_object(self, queryset=None):
        blog = super().get_object(queryset)
        blog.view_count += 1
        blog.save()

        return blog


class BlogPostCreateView(CreateView):
    model = BlogPost
    template_name = 'catalog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'published']
    success_url = reverse_lazy('catalog:blogpost_list')

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save(commit=False)
            print(f"Before: Title: {blog.title}, Slug: {blog.slug}")
            blog.slug = slugify(blog.title)
            print(f"After: Title: {blog.title}, Slug: {blog.slug}")
            blog.save()

        return super().form_valid(form)


class BlogPostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'catalog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'published']

    def form_valid(self, form):
        if form.is_valid():
            blog = form.save(commit=False)
            print(f"Before: Title: {blog.title}, Slug: {blog.slug}")
            blog.slug = slugify(blog.title)
            print(f"After: Title: {blog.title}, Slug: {blog.slug}")
            blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blogpost_detail', args=[self.kwargs.get('slug')])


class BlogPostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'catalog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('catalog:blogpost_list')
