from django.shortcuts import render
from products.models import Product

def index(request):
    products = Product.objects.all().order_by('-created_at')[:6]
    context = {
        'products':products
    }
    if request.htmx:
        return render(request, 'core/parts/_index.html', context)
    
    return render(request, 'core/index.html', context)
def about(request):
    if request.htmx:
        return render(request, 'core/parts/_about.html')
    return render(request, 'core/about.html')
