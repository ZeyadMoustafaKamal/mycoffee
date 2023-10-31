from django.db import models
from django.urls import reverse
from django.utils import timezone

from .fields import RandomField


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='product_images', max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return '{}'.format(self.name)

    def get_absolute_url(self):
        return reverse("product_details", kwargs={"pk": self.pk})


class Cart(models.Model):
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='cart'
    )
    orders = models.ManyToManyField('Order')

    def empty_cart(self):
        # After the user checks out delete orders from here
        # The orders will stay in the database for furure use but Just delete them from the 'orders' relationship
        for order in self.orders:
            self.orders.remove(order)


class Order(models.Model):
    class OrderStatus(models.Choices):
        pending = 'Pending'
        shipped = 'Shipped'
        done = 'Done'
        canceled = 'Canceled'
    id = RandomField(primary_key=True)  # noqa: A003
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(
        max_length=50,
        choices=OrderStatus.choices,
        default=OrderStatus.pending
    )
    shipping_address = models.TextField()
    transaction_id = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )  # I should get this from the payment provider

    items = models.ManyToManyField('products.OrderItem')
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def get_order_price(self):
        cost = 0
        for item in self.items.all():
            cost += item.get_total_price
        return cost

    def __str__(self):
        return f'{self.user.first_name} ({self.status})'


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    discount = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        max_length=100
    )  # it may be like 80.00 so its a 80% discount

    @property
    def shipping_cost(self):
        # Should be changed to a dynamic value
        return 10

    @property
    def get_total_price(self):
        products_price = self.product.price * self.quantity

        if self.discount:
            discounted_price = self.discount / 100 * products_price
            products_price -= - discounted_price
        total_price = products_price + self.shipping_cost
        return total_price
