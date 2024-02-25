from django.shortcuts import render
from products.models import Product, Category


def home_page(request):
    recent_products = Product.objects.filter(allowed=True)[:6]
    categories = Category.objects.all()
    return render(request, 'home/index.html', context={'products': recent_products, 'categories': categories})


def about_us_page(request):
    return render(request, 'home/about.html', context={})


def contact_us_page(request):
    return render(request, 'home/contact.html', context={})
