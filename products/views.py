from django.shortcuts import render
from .models import Product, Category


def all_products(request):
    products = Product.objects.filter(allowed=True)
    categories = Category.objects.all()
    return render(request, 'products/products.html', context={'products': products, 'categories': categories})


def product_detail(request, id, slug):
    product = Product.objects.get(id=id, slug=slug)
    categories = Category.objects.all()
    return render(request, 'products/detail.html', context={'product': product, 'categories': categories})

