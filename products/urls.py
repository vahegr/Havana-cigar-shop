from django.urls import path, include, re_path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products, name='products'),
    path('product-detail/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('cart-products', views.cart_products, name='cart_products'),
    path('cart-add-product/<int:id>', views.CartAddView.as_view(), name='cart_add_products'),
    path('remove-cart-product/<str:id>', views.CartRemoveView.as_view(), name='remove_cart_product'),
]
