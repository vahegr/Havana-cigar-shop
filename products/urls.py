from django.urls import path, include, re_path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.all_products_view, name='products'),
    path('product-detail/<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
    path('cart-products', views.cart_products, name='cart_products'),
    path('cart-add-product/<int:id>', views.CartAddView.as_view(), name='cart_add_products'),
    path('remove-cart-product/<str:id>', views.CartRemoveView.as_view(), name='remove_cart_product'),
    path('order-detail/<int:id>', views.OrderDetailView.as_view(), name='order_detail'),
    path('order-add', views.order_create, name='order_add'),
    path('category-detail/<int:id>/<slug:slug>', views.category_detail, name='category_detail'),
]
