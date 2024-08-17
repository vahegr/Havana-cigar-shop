from unicodedata import decimal

from products.models import Product

CART_SESSION_ID = 'cart'


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def __iter__(self):
        cart = self.cart.copy()
        for item in cart.values():
            product = Product.objects.get(id=int(item['id']))
            item['product'] = product
            item['total'] = int(item['quantity']) * float(item['price'])
            item['unique_id'] = self.unique_id_generator(product.id, item['state_of_product'])
            yield item

    def unique_id_generator(self, id, state_of_product):
        result = f'{id}-{state_of_product}'
        return result

    def clear_cart(self):
        del self.session[CART_SESSION_ID]

    def add(self, product, quantity, state_of_product):
        unique = self.unique_id_generator(product.id, state_of_product)
        if unique not in self.cart:
            if state_of_product == 'Box':
                self.cart[unique] = {'quantity': 0, 'price': float(product.price), 'state_of_product': state_of_product, 'id': product.id}
            else:
                self.cart[unique] = {'quantity': 0, 'price': float(product.single_cigar_price), 'state_of_product': state_of_product, 'id': product.id}
        self.cart[unique]['quantity'] += int(quantity)
        self.save()

    def total(self):
        cart = self.cart.values()
        total = sum(float(item['price']) * item['quantity'] for item in cart)
        # total = 0
        # for item in cart:
        #     total += float(item['total'])
        return total

    def delete(self, id):
        if id in self.cart:
            del self.cart[id]
            self.save()

    def save(self):
        self.session.modified = True

