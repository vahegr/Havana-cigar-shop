from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.core.paginator import Paginator
from .models import Product, Category, Order, OrderItem
from .cart_module import Cart
from .forms import OrderCreationForm


def all_products_view(request):
    all_products = Product.objects.filter(allowed=True)
    categories = Category.objects.all()
    pagination = Paginator(all_products, 9)
    page = request.GET.get('page')
    products = pagination.get_page(page)
    return render(request, 'products/products.html', context={'products': products, 'categories': categories})


def product_detail(request, id, slug):
    product = Product.objects.get(id=id, slug=slug)
    categories = Category.objects.all()
    return render(request, 'products/detail.html', context={'product': product, 'categories': categories})


def category_detail(request, id, slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, id=id, slug=slug)
    all_product = category.product_set.all()
    pagination = Paginator(all_product, 9)
    page = request.GET.get('page')
    products = pagination.get_page(page)
    return render(request, "products/products.html", context={'products': products, 'categories': categories})


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


class OrderDetailView(View):
    def get(self, request, id):
        pass


def order_create(request):
    form = OrderCreationForm()
    return render(request, 'products/order-create.html', context={'form': form})


# class OrderCreateView(View):
#     def get(self, request):
#         cart = Cart(request)
#         order = Order.objects.create(user=request.user)
#         for item in cart:
#             OrderItem.objects.create(order=order, product=item['product'], state_of_product=item['state_of_product'], quantity=item['quantity'], price=item['price'])
#         return redirect('products:order_detail', order.id)


