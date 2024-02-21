from django.shortcuts import render, redirect, reverse
from django.views import View
from .models import Product, Category
from .cart_module import Cart


def all_products(request):
    products = Product.objects.filter(allowed=True)
    categories = Category.objects.all()
    return render(request, 'products/products.html', context={'products': products, 'categories': categories})


def product_detail(request, id, slug):
    product = Product.objects.get(id=id, slug=slug)
    categories = Category.objects.all()
    return render(request, 'products/detail.html', context={'product': product, 'categories': categories})


def cart_products(request):
    cart = Cart(request)
    return render(request, 'products/cart-products.html', context={'cart': cart})


class CartAddView(View):
    def post(self, request, id):
        product = Product.objects.get(id=id)
        quantity, state_of_product = request.POST.get('quantity'), request.POST.get('state_of_product')
        cart = Cart(request)
        cart.add(product, quantity, state_of_product)
        return redirect('products:cart_products')


class CartRemoveView(View):
    def get(self, request, id):
        cart = Cart(request)
        cart.delete(id)
        return redirect('products:cart_products')



