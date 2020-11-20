from django.shortcuts import get_object_or_404

from spaweb.models import Product


def send_message(request):
    cart = request.session['cart']
    cart_products = []
    total_price = 0
    cart_products_amount = 0
    for key in cart:
        product = get_object_or_404(Product, pk=key)
        total_price += product.price * cart[key]
        
        cart_products.append({
            'product': product,
            'quantity': cart[key],
        })

        cart_products_amount += cart[key]
    return {
        'cart_products': cart_products,
        'total_price': total_price,
        'cart_products_amount': cart_products_amount
    }