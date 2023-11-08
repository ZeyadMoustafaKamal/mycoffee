from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Case, CharField, Value, When
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView

from core.mixins import SuccessMessageMixin
from htmx.mixins import HTMXRedirectMixin, HTMXTemplateMixin
from products.models import Product

from .forms import AddToCartForm
from .models import Order


class AddToCartView(
    HTMXTemplateMixin,
    HTMXRedirectMixin,
    LoginRequiredMixin,
    SuccessMessageMixin,
    FormView
):
    template_name = 'orders/add_to_cart.html'
    htmx_template = 'orders/parts/_add_to_cart.html'
    login_url = reverse_lazy('login')
    form_class = AddToCartForm
    _product = None

    def form_valid(self, form):
        form.product = self.get_product()
        form.user = self.request.user
        form.save_instance()
        return super().form_valid(form)

    def get_product(self):
        if not self._product:
            self._product = get_object_or_404(Product, id=self.kwargs.get('id'))
        return self._product

    def get_success_url(self):
        product = self.get_product()
        return product.get_absolute_url()

    def get_success_message(self):
        form = self.get_form()
        quantity = form.cleaned_data.get('quantity')
        msg = 'Added %s "%s" to your cart' % (quantity, self.get_product().name)
        return msg


class OrderListView(HTMXTemplateMixin, LoginRequiredMixin, ListView):
    template_name = 'orders/all.html'
    htmx_template = 'ordres/parts/_all.html'
    model = Order
    context_object_name = 'orders'

    def get_queryset(self):
        """ prefetech related item from the "Order" and order the "Order" queryset
            depending on thier status
        """
        qs = super().get_queryset().filter(user=self.request.user).prefetch_related('items')
        status_values = {
            value: index for index, value in enumerate(Order.StatusChoices.values)
        }
        order_conditions = [When(status=status, then=Value(order)) for status, order in status_values.items()]
        qs = qs.annotate(
            status_number=Case(
                *order_conditions,
                default=Value(5),
                output_field=CharField()
            )
        ).order_by('status_number', '-created_at')
        return qs
