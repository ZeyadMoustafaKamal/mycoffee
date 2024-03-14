from django.contrib.auth import get_user_model
from django.db import models

from orders.cart.models import Cart  # noqa: F401
from products.models import Product

from .fields import RandomField
from .managers import OrderManager

User = get_user_model()


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        pending = 'Pending'
        shipped = 'Shipped'
        done = 'Done'
        canceled = 'Canceled'
    id = RandomField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=100, choices=StatusChoices.choices, default=StatusChoices.pending)

    objects = OrderManager()

    def __str__(self):
        return f'{self.user.first_name}, {self.status}'

    @property
    def get_total(self):
        return sum([item.get_total for item in self.items.all()])


class OrderItem(models.Model):
    id = RandomField(primary_key=True, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=5, decimal_places=2)  # The price if there is no discount
    discounted_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True
    )  # The price after the discount if any
    quantity = models.IntegerField(default=0)

    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250)
    city = models.CharField(max_length=70)
    state = models.CharField(max_length=70)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return 'order number {}'.format(self.id)

    @property
    def get_price(self):
        if self.discounted_price:
            return self.discounted_price
        return self.price

    @property
    def get_dicount_percentage(self):
        return '{}%'.format(self.discounted_price / self.price * 100)

    @property
    def get_total(self):
        return self.get_price * self.quantity

    @property
    def get_status(self):
        return self.order.status
