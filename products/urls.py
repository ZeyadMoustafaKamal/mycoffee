from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.ListProductsView.as_view(), name='list_products'),
    path('<pk>', views.product_details, name='product_details'),
    path('search/', views.search_view, name='search')
]

