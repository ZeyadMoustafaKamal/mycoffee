from django.urls import path

from . import views

urlpatterns = [
    path('add_to_cart/<id>/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', views.CartView.as_view(), name='cart')
]
