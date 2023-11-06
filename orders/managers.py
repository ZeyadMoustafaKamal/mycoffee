from django.db import models


class OrderManager(models.Manager):

    def create_or_get_for_user(self, user):
        """ Used to create or get an Order instance from the given user
        and do some related things like adding it to the cart
        """
        cart = user.get_cart()
        if cart.order is not None:
            return cart.order
        order = self.create(user=user)
        cart.order = order
        cart.save()
        return order
