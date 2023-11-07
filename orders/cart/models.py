from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    # This is OneToOne field because every time the user will be able to make one order
    # and every order can have more than one OrderItem instance so that the process may be easier
    order = models.OneToOneField('Order', on_delete=models.CASCADE, null=True)

    def empty_cart(self):
        self.order = None
        self.save()
