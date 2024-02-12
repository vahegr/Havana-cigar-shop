from django.urls import path, include, re_path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='products'),
    path('product-detail/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('cart-products', views.cart_products, name='cart_products'),
]
