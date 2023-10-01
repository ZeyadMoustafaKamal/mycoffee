from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django_filters.views import FilterView

from accounts.models import UserProfile
from core.utils import render_htmx
from core.mixins import HTMXTemplateMixin

from .models import Product
from .filters import ProductFilter

class ListProductsView(HTMXTemplateMixin, FilterView):
    model = Product
    template_name = 'products/list.html'
    htmx_template = 'products/parts/_list.html'
    context_object_name = 'products'
    filterset_class = ProductFilter


def product_details(request, pk):
    is_favourite = False
    product = get_object_or_404(Product, pk=pk)
    context = {
        'product':product,
        'is_favourite':is_favourite
    }
    if request.user.is_authenticated:
        profile = UserProfile.objects.prefetch_related('favourites').get(pk=request.user.pk)
        if request.method == 'POST' and 'favourite' in request.POST:
            return JsonResponse(profile.toggle_product(product))
        is_favourite = product in profile.favourites.all()
        context['is_favourite'] = is_favourite
    return render_htmx(
        request, 
        'products/details.html', 
        'products/parts/_details.html', 
        context
    )
def search_view(request):
    filter = ProductFilter()
    return render(request, 'products/search.html', {'filter':filter})

