import json
from statistics import mode

from django.core.management.base import BaseCommand

from authapp.models import User
# from mainapp.models import Product, ProductCategory


def load_from_json(file_name):
    with open(file_name, encoding='utf-8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    help = 'Fill data in db'

    def add_arguments(self, parser):
        parser.add_argument('-m', '--model', help='model list input',
                            type=lambda s: [str(item) for item in s.split('+')])

    def handle(self, *args, **options):
        model = options['model']
        print(model)
        items = load_from_json(f'mainapp/json/{model[0]}.json')
        print(items)
        print('*'*100)
        for item in items:
            User.objects.create(**item)

        # items = load_from_json('mainapp/json/products.json')
        # for item in items:
        #     category = ProductCategory.objects.get(name=item['category'])
        #     item['category'] = category
        #     Product.objects.create(**item)

    if not User.objects.filter(username='am').exists():
        User.objects.create_superuser(
            'am', 'ktyjxrf')
