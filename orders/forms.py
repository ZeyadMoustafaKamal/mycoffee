from django import forms
from django.forms.models import model_to_dict

from core.bootstrap.forms import BootstrapForm

from .models import Order, OrderItem


class AddToCartForm(BootstrapForm, forms.Form):
    quantity = forms.IntegerField()

    def save_instance(self):
        """ Used to manage the creation process of the OrderItem """

        if not hasattr(self, 'product') or not hasattr(self, 'user'):  # Make sure every thing is okay
            raise ValueError("You must add a product and a user instance before you create and OrderItem instance")

        order_item, created = self.get_or_create_order(self.user, self.product)
        if created:
            # Get some data from the user instance like the address and zip code, ect..
            user_data = model_to_dict(self.user.profile, fields=[
                'address1',
                'address2',
                'city',
                'state',
                'zip_code'
            ])
            for k, v in user_data.items():
                setattr(order_item, k, v)
        order_item.quantity += self.cleaned_data.get('quantity')
        order_item.save()
        return order_item

    def get_or_create_order(self, user, product):
        """ Used to create OrderItem instance or get an existing one
        This is essential if for example the user wants to buy the product "x" and made another order to buy
        the product "x" again as in this case I will just add the new quantity to an existing Orderitem
        """
        order = Order.objects.create_or_get_for_user(user)
        try:
            order_item = order.items.get(product__id=product.id, price=product.price)  # Maybe the price is changed
        except OrderItem.DoesNotExist:
            return OrderItem(product=product, price=product.price, order=order), True
        else:
            return order_item, False
