from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages
from .utils import slugify

from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import ProductForm, VersionForm
from .models import Product, Category, BlogPost, Version


class HomeView(LoginRequiredMixin, TemplateView):
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


class ContactsView(LoginRequiredMixin, TemplateView):
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


class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'object_list'
    template_name = 'catalog/categories.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'КАТАЛОГ'
        return context

    def get_queryset(self):
        return super().get_queryset().order_by('name')


class ProductDetailView(LoginRequiredMixin, DetailView):
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


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')
    permission_required = 'catalog.add_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request'] = self.request
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1, can_delete=True)

        if self.request.method == "POST":
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)

        return context

    def form_valid(self, form):
        with transaction.atomic():
            self.object = form.save(commit=False)

            user = self.request.user
            self.object.owner = user
            self.object.save()

            formset = self.get_context_data()['formset']
            formset.instance = self.object

            if form.is_valid() and formset.is_valid():
                versions = formset.save(commit=False)  # Сохраняем версии без немедленного фиксирования

                for version in versions:
                    version.product = self.object  # Устанавливаем ссылку на сохраненный товар
                    version.save()  # Фиксируем каждую версию

            messages.success(self.request, 'Товар успешно создан')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_list')


class ProductListView(LoginRequiredMixin, ListView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'СПИСОК ТОВАРОВ'
        return context


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')
    permission_required = 'catalog.change_product'

    def get_form_kwargs(self):
        kwargs = super(ProductUpdateView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        print(self.request.user.get_all_permissions())
        print(self.request.user)
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1, can_delete=True)

        if self.request.method == "POST":
            context['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context['formset'] = VersionFormset(instance=self.object)

        context['request'] = self.request
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if form.is_valid() and formset.is_valid():
            formset.instance = self.object
            formset.save()

        messages.success(self.request, 'Товар успешно обновлен')

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')
    permission_required = 'catalog.delete_product'


class BlogPostListView(LoginRequiredMixin, ListView):
    model = BlogPost
    template_name = 'catalog/blogpost_list.html'
    context_object_name = 'blogposts'

    # paginate_by = 3

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(published=True)
        queryset = queryset.order_by('created_at')

        return queryset


class BlogPostDetailView(LoginRequiredMixin, DetailView):
    model = BlogPost
    template_name = 'catalog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get_object(self, queryset=None):
        blog = super().get_object(queryset)
        blog.view_count += 1
        blog.save()

        return blog


class BlogPostCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = BlogPost
    template_name = 'catalog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'published']
    success_url = reverse_lazy('catalog:blogpost_list')
    permission_required = 'catalog.view_blogpost'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Применяем класс CSS "form-control" ко всем полям формы
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'published':
                field.widget.attrs['class'] = 'form-check-input'
        return form

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if form.is_valid() and formset.is_valid():
            formset.instance = self.object
            blog = formset.save(commit=False)
            print(f"Before: Title: {blog.title}, Slug: {blog.slug}")
            blog.slug = slugify(blog.title)
            print(f"After: Title: {blog.title}, Slug: {blog.slug}")
            blog.save()

        return super().form_valid(form)


class BlogPostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = BlogPost
    template_name = 'catalog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'published']
    permission_required = 'catalog.change_blogpost'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Применяем класс CSS "form-control" ко всем полям формы
        for field_name, field in form.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'published':
                field.widget.attrs['class'] = 'form-check-input'
        return form

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if form.is_valid() and formset.is_valid():
            formset.instance = self.object
            blog = formset.save(commit=False)
            print(f"Before: Title: {blog.title}, Slug: {blog.slug}")
            blog.slug = slugify(blog.title)
            print(f"After: Title: {blog.title}, Slug: {blog.slug}")
            blog.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('catalog:blogpost_detail', args=[self.kwargs.get('slug')])


class BlogPostDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = BlogPost
    template_name = 'catalog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('catalog:blogpost_list')
    permission_required = 'catalog.delete_blogpost'
