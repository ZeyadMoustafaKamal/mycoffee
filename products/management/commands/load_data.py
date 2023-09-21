from django.core.management import BaseCommand
from django.core.files.base import ContentFile
import time
from products.models import Product

import random
import requests

class Command(BaseCommand):
    def handle(self, *args, **options):
        Product.objects.all().delete() # Delete all products and then get them again
        url = 'https://api.sampleapis.com/coffee/hot/'
        products = requests.get(url).json()

        for product in products:
            name = product['title']
            description = product['description']
            image = product['image']
        
            price = ''.join([str(random.randint(1, 9)) for _ in range(4)])
            formated_price = float('{}.{}'.format(price[:2], price[2:]))
            prod = Product(name=name, description=description, price=formated_price)
            req = requests.get(image)
            if req.status_code == 200:
                image_data = ContentFile(req.content)
                prod.image.save('{}.jpg'.format(name), image_data)
                prod.save()

        self.stdout.write('Success!!')



