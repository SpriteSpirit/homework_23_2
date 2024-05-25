from django import forms
from .models import Product, BlogPost

FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа',
                   'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'image', 'price']

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
