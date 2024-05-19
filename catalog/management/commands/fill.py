import json

from django.core.management import BaseCommand
from catalog.models import Category, Product


class Command(BaseCommand):

    @staticmethod
    def json_read_categories():
        categories = []
        # Здесь мы получаем данные из фикстур с категориями
        with open('db.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "catalog.category":
                    categories.append(item)

        return categories

    @staticmethod
    def json_read_products():
        products = []
        # Здесь мы получаем данные из фикстур с продуктами
        with open('db.json', 'r', encoding='utf-8') as file:
            data = json.load(file)

            for item in data:
                if item.get('model') == "catalog.product":
                    products.append(item['fields'])

        return products

    def handle(self, *args, **options):

        # Удаление всех продуктов
        Product.objects.all().delete()
        # Удаление всех категорий
        Category.objects.all().delete()

        # Создайте списки для хранения объектов
        product_for_create = []
        category_for_create = []

        # Обходим все значения категорий из фикстуры для получения информации об одном объекте
        for category in Command.json_read_categories():
            category_for_create.append(Category(pk=category['pk'],
                                                name=category['fields']['name'],
                                                description=category['fields']['description']))

        # Создаем объекты в базе с помощью метода bulk_create()
        Category.objects.bulk_create(category_for_create)

        # Обходим все значения продуктов из фикстуры для получения информации об одном объекте
        for product in Command.json_read_products():
            product_for_create.append(Product(name=product['name'],
                                              description=product['description'],
                                              image=product['image'],
                                              category=Category.objects.get(pk=product['category']),
                                              price=product['price']))

        print(product_for_create)

        # Создаем объекты в базе с помощью метода bulk_create()
        Product.objects.bulk_create(product_for_create)
