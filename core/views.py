from htmx.base import render_htmx

from products.models import Product


def index(request):
    products = Product.objects.all().order_by('-created_at')[:6]
    context = {
        'products':products
    }
    return render_htmx(request, 'core/index.html', 'core/parts/_index.html', context)
def about(request):
    return render_htmx(request, 'core/about.html', 'core/parts/_about.html', )
