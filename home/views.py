from django.shortcuts import render
from products.models import Product


def home_page(request):
    recent_products = Product.objects.filter(allowed=True)[:6]
    return render(request, 'home/index.html', context={'products': recent_products})
