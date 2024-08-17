from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic import ListView
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
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
    similar_products = Product.objects.filter(category=product.category.first())
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


# def order_create(request):
#     if request.method == 'POST':
#         form = OrderCreationForm(request.POST)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             return redirect(reverse('products:order_item_create', args=[instance.id]))
#         else:
#             form = OrderCreationForm()
#         return render(request, 'products/order-create.html', context={'form': form})


class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, id):
        order = Order.objects.get(id=id)
        if order.user_id == request.user.id or request.user.is_admin:
            return render(request, 'products/order-detail.html', context={'order': order})
        else:
            return redirect('home:home')


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = float(cart.total())
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order, product=item['product'], state_of_product=item['state_of_product'], quantity=item['quantity'], price=item['price'])
                cart.clear_cart()

                # send an email to the owner of the website that he gets an new order.
                send_to_owner_mail_subject = f'New Order, Customer email:{form.cleaned_data.get("email_address")}'
                send_to_owner_message = f'new order click the link to see the details: https://rarecubancigars.org/products/order-detail/{order.id}'

                send_to_owner_email = EmailMessage(
                    send_to_owner_mail_subject, send_to_owner_message, to=['vahegrigorian447@gmail.com']
                )
                send_to_owner_email.send()

                # send an email to the customer email address that he ordered his stuff successfuly.
                send_to_customer_mail_subject = 'Your order has been successfully placed'
                send_to_customer_message = f'Your order has been successfully placed. click the link to see the details: https://rarecubancigars.org/products/order-detail/{order.id}'

                send_to_customer_email = EmailMessage(
                    send_to_customer_mail_subject, send_to_customer_message, to=[form.cleaned_data.get('email_address')]
                )
                send_to_customer_email.send()
            return redirect('products:order_detail', order.id)
    else:
        form = OrderCreationForm()
    return render(request, 'products/order-create.html', context={'form': form})


# class OrderItemCreateView(View):
#     def get(self, request):
#         cart = Cart(request)
#         for item in cart:
#             OrderItem.objects.create(order=order, product=item['product'], state_of_product=item['state_of_product'], quantity=item['quantity'], price=item['price'])
#         return redirect('products:order_detail', order.id)


