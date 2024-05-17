from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.urls import reverse
from django.views.generic import TemplateView, ListView, DetailView, CreateView

from .forms import ProductForm
from .models import Product, Category


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
        return redirect('object_list')

    def get_success_url(self):
        return reverse('object_list')


def get_product_list(request):
    product_list = Product.objects.order_by('created_at')
    paginator = Paginator(product_list, 10)
    page = request.GET.get('page')

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'title': 'Список товаров',
        'object_list': products,
    }

    return render(request, 'catalog/product_list.html', context)
