from django.core.management import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product

import random
import requests


class Command(BaseCommand):
    """ I was using this command before and every time I build the image I get the products again but this is really
        bad practice so I decided to make a fixture for this and just load the data using that fixure
        but I will still let this here.
    """
    def handle(self, *args, **options):
        Product.objects.all().delete()  # Delete all products and then get them again
        url = 'https://api.sampleapis.com/coffee/hot/'
        products = requests.get(url).json()

        for product in products:
            name = product['title']
            description = product['description']
            image = product['image']

            price = random.uniform(10, 100)
            prod = Product(name=name, description=description, price=round(price, 2))
            req = requests.get(image)
            if req.status_code == 200:
                image_data = ContentFile(req.content)
                prod.image.save('{}.jpg'.format(name), image_data)
                prod.save()

        self.stdout.write('Success!!')
