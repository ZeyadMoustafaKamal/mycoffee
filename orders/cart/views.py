from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views.generic import ListView, View

from htmx.mixins import HTMXTemplateMixin
from orders.models import Order


class CartView(
    HTMXTemplateMixin,
    ListView
):
    """ A class to view the OrderItems in the cart """
    template_name = 'orders/cart.html'
    htmx_template = 'orders/parts/_cart.html'
    context_object_name = 'order_items'
    _order = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.get_order()
        context.update({
            'order': order
        })
        return context

    def get_queryset(self):
        order = self.get_order()
        if order:
            return order.items.all().select_related('product', 'order')
        return Order.objects.none()

    def get_order(self):
        if self._order is not None:
            return self._order
        order = self.request.user.cart.order
        if order is not None:
            self._order = order
            return self._order
        return Order.objects.none()


class CheckoutView(LoginRequiredMixin, View):
    def post(self, *args, **kwargs):
        cart = self.request.user.get_cart()
        if cart.order is not None:
            cart.order = None
            cart.save()
        return redirect('index')
