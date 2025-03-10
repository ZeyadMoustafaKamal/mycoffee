from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django_filters.views import FilterView

from accounts.models import UserProfile
from htmx.base import render_htmx
from htmx.mixins import HTMXTemplateMixin

from .filters import ProductFilter
from .models import Product

User = get_user_model()


class ListProductsView(HTMXTemplateMixin, FilterView):
    model = Product
    template_name = 'products/list.html'
    htmx_template = 'products/parts/_list.html'
    context_object_name = 'products'
    filterset_class = ProductFilter


def product_details(request, pk):

    product = get_object_or_404(Product, pk=pk)
    is_favourite = False

    if request.user.is_authenticated:
        profile = UserProfile.objects.prefetch_related('favourites').get(user=request.user)

        is_favourite = product in profile.favourites.all()
        if 'favourite' in request.POST:
            is_favourite = profile.toggle_product(product)

    context = {
        'product': product,
        'is_favourite': is_favourite
    }
    return render_htmx(
        request,
        'products/details.html',
        'products/parts/_details.html',
        context
    )


def search_view(request):
    filter = ProductFilter()
    return render_htmx(
        request,
        'product/search.html',
        'products/parts/_search.html',
        {
            'filter': filter
        }
    )
