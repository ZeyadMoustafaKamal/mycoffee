from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django_filters.views import FilterView

from accounts.models import UserProfile

from .models import Product
from .filters import ProductFilter

class ListProductsView(FilterView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    filterset_class = ProductFilter

    

def product_details(request, pk):
    is_favourite = None
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated:
        profile = UserProfile.objects.prefetch_related('favourites').get(pk=request.user.pk)
        if request.method == 'POST' and 'favourite' in request.POST:
            return JsonResponse(profile.toggle_product(product))
        is_favourite = product in profile.favourites.all()

    return render(request, 'products/details.html', {'product':product, 'is_favourite':is_favourite})
def search_view(request):
    filter = ProductFilter()
    return render(request, 'products/search.html', {'filter':filter})

