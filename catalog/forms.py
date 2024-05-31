from django import forms
from django.core.exceptions import ValidationError
from django.db import transaction

from .models import Product, BlogPost, Version

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа',
                   'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label

            if field_name == 'is_current':
                field.widget.attrs['class'] = 'form-check-input'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data['name']

        if any(word in name.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError('Нельзя использовать запрещенные слова')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']

        if any(word in description.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError('Нельзя использовать запрещенные слова')
        return description


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'preview', 'published']

    def clean_title(self):
        title = self.cleaned_data['title']

        if any(word in title.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError('Нельзя использовать запрещенные слова')
        return title


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        product = self.cleaned_data.get('product')

        # Проверяем, если это новая запись
        if instance.pk is None:
            # Обновите другие текущие версии для продукта, прежде чем устанавливать текущую версию
            with transaction.atomic():
                Version.objects.filter(product=product, is_current=True).update(is_current=False)

        instance.is_current = True
        if commit:
            instance.save()

        return instance

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        version_number = cleaned_data.get('version_number')

        # Проверка уникальности версии для продукта
        if Version.objects.filter(product=product, version_number=version_number).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('Такая версия уже существует для этого продукта.')

        return cleaned_data
