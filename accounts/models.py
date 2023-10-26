from django.db import models
from django.contrib.auth.models import AbstractUser

from products.models import Product


class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=70)
    zip_code = models.CharField(max_length=10)
    favourites = models.ManyToManyField(Product)

    def __str__(self):
        return '{} profile'.format(self.user.first_name)

    def toggle_product(self, product):
        """ Used to add/remove the product from the favourites """
        favourite = True
        if product in self.favourites.all():
            self.favourites.remove(product)
            favourite = False
        else:
            self.favourites.add(product)
        return favourite
