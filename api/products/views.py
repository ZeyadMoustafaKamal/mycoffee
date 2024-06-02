from rest_framework import viewsets

from api.mixins import PaginatedResponseMixin
from products.models import Product

from .serializers import ProductSerializer


class ProductsViewset(viewsets.ReadOnlyModelViewSet, PaginatedResponseMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
