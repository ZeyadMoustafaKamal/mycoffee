from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.v1.products.views import ProductsViewset

router = DefaultRouter()

router.register('products', ProductsViewset)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
] + router.urls
