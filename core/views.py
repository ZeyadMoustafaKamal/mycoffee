from django.shortcuts import render
from products.models import Product

def index(request):
    products = Product.objects.all().order_by('-created_at')[:6]
    return render(request, 'core/index.html', {'products':products})
def about(request):
    return render(request, 'core/about.html')


