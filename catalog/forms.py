from django import forms
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
        fields = ['name', 'description', 'category', 'image', 'price']
        exclude = ('owner',)

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


class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        product = self.cleaned_data.get('product')

        # Проверяем, если это новая запись
        if instance.pk is None:
            # Убедимся, что нет других текущих версий для продукта перед обновлением
            with transaction.atomic():
                Version.objects.filter(product=product, is_current=True).update(is_current=False)
                instance.is_current = True
                if commit:
                    instance.save()
        else:
            # Если это обновление существующей записи, оставляем все как есть по умолчанию
            if commit:
                instance.save()

        return instance

    def clean(self):
        cleaned_data = super().clean()
        product = cleaned_data.get('product')
        is_current = cleaned_data.get('is_current')

        if is_current:
            if self.instance.pk is None:  # Проверяем, что экземпляр не новый
                Version.objects.filter(product=product).exclude(pk=self.instance.pk).update(is_current=False)
                raise forms.ValidationError("Необходимо сохранить версию перед установкой ее в качестве активной.")

            existing_current_versions = Version.objects.filter(product=product, is_current=True)

            if existing_current_versions.exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError('Только одна версия может быть активной')

            return cleaned_data
