def add_to_cart(request):
    product_id = request.POST.get('add_product_id')
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(product_id)
        if quantity:
            cart[product_id] = quantity + 1
        else:
            cart[product_id] = 1
    else:
        cart = {}
        cart[product_id] = 1
    request.session['cart'] = cart
    print(request.session['cart'])