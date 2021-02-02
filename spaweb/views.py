from datetime import datetime
from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from spaweb.models import Product, ProductCategory, Topic, Order, OrderItem, Customer
from django.core.mail import send_mail
from formulaspa.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404
import requests
from environs import Env
env = Env()
env.read_env()


def index(request):
    bestsellers = Product.objects.filter(is_bestseller=True).prefetch_related('category')
    certificates = Product.objects.filter(category__name='Сертификаты').order_by('price')

    context = {
        "bestsellers": bestsellers,
        "certificates": certificates,
    }
    return render(request, "index.html", context)


def contact(request):
    return render(request, "contact.html")


def product_detail(request, slug):
    try:
        cart = request.session['cart']
    except KeyError:
        cart = {}
    product = get_object_or_404(Product, slug=slug)
    product_category = product.category
    related_products = Product.objects.filter(category=product_category)

    context = {
        'product': product,
        'related_products': related_products,
        'cart': cart,
    }
    return render(request, "product-detail.html", context)


def product_listing(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    categories = ProductCategory.objects.all()
    topics = Topic.objects.all()
    products = Product.objects.all()
    if request.method == "POST":
        minprice = request.POST.get('minprice')
        maxprice = request.POST.get('maxprice')
        if minprice or maxprice:
            products_by_category = products.filter(
                category=category, price__range=(minprice, maxprice))
        else:
            minprice = "0"
            maxprice = "15000"
            products_by_category = products.filter(
                category=category, price__range=(minprice, maxprice))
    else:
        products_by_category = products.filter(category=category)

    context = {
        'products_by_category': products_by_category,
        'categories': categories,
        'topics': topics,
        'category': category,
    }
    return render(request, 'category.html', context)


def get_topic_listing(request, slug):
    topic = get_object_or_404(Topic, slug=slug)
    categories_by_topic = ProductCategory.objects.filter(topic=topic)
    if request.method == "POST":
        minprice = request.POST.get('minprice')
        maxprice = request.POST.get('maxprice')
        if minprice or maxprice:
            products_by_topic = Product.objects.filter(
                category__in=categories_by_topic,
                price__range=(minprice, maxprice))
        else:
            minprice = "0"
            maxprice = "15000"
            products_by_topic = Product.objects.filter(
                category__in=categories_by_topic,
                price__range=(minprice, maxprice))
    else:
        products_by_topic = Product.objects.filter(
            category__in=categories_by_topic)

    context = {
        'topic': topic,
        'categories_by_topic': categories_by_topic,
        'products_by_topic': products_by_topic,
    }

    return render(request, 'topic.html', context)


def search(request):
    query = request.POST.get('q')
    queryset = []
    if query:
        queries = query.split(' ')
        for q in queries:
            q_upper = q.upper()
            q_lower = q.lower()
            products = Product.objects.filter(
                Q(name__icontains=q_upper) |
                Q(name__icontains=q_lower) |
                Q(description__icontains=q_upper) |
                Q(description__icontains=q_lower)
            ).distinct()

            for product in products:
                queryset.append(product)

    context = {
        'products_by_category': set(queryset),
    }
    return render(request, "search.html", context)


def cart(request):
    try:
        cart = request.session['cart']
    except KeyError:
        cart = {}
    total_price = 0
    cart_products = []
    cities = []

    for key in cart:
        product = get_object_or_404(Product, pk=key)
        product_cost = product.price * cart[key]
        total_price += product_cost
        if product.city not in cities:
            cities.append(product.city)
        cart_products.append({
            'product': product,
            'quantity': cart[key],
            'product_cost': product_cost,
        })
    if len(cities) > 1:
        is_cities_correct = False
    else:
        is_cities_correct = True

    context = {
        'cart_products': cart_products,
        'total_price': total_price,
        'is_cities_correct': is_cities_correct,
    }
    return render(request, "shop-cart.html", context)


def add_to_cart(request, slug):
    request.session.set_expiry(60 * 60)
    product = get_object_or_404(Product, slug=slug)
    cart = request.session.get('cart')
    if cart:
        quantity = cart.get(product.id)
        if quantity:
            cart[product.id] = quantity + 1
        else:
            cart[product.id] = 1
    else:
        cart = {}
        cart[product.id] = 1

    request.session['cart'] = cart

    return redirect(reverse('product-detail', kwargs={'slug': slug}))


def remove_cart_item(request, pk):
    cart = request.session['cart']
    product_id = str(pk)
    cart.pop(product_id)
    request.session['cart'] = cart
    if request.method == 'POST':
        button_spot = request.POST.get('trash')
        if button_spot == 'header_trash':
            return redirect(reverse('index'))
        if button_spot == 'cart_trash':
            return redirect(reverse('cart'))

    return render(request, "index.html")


def change_item_quantity(request, pk):
    cart = request.session['cart']
    product_id = str(pk)
    if request.method == 'POST':
        quantity_button = request.POST.get('quantity')
        if quantity_button == 'minus':
            quantity = cart.get(product_id) - 1
            if quantity == 0:
                quantity = 1
        elif quantity_button == 'plus':
            quantity = cart.get(product_id) + 1
        
        cart[product_id] = quantity
        request.session['cart'] = cart
    return redirect(reverse('cart'))


def promo(request):
    return render(request, "promo.html")


def declarations(request):
    return render(request, "declarations.html")


def faq(request):
    return render(request, "faq.html")


def checkout(request):
    try:
        cart = request.session['cart']
    except KeyError:
        return redirect(reverse('index'))
    cart_products = []
    total_price = 0
    for key in cart:
        product = get_object_or_404(Product, pk=key)
        price = product.price
        quantity = cart[key]
        cart_products.append({
            'product': product,
            'quantity': quantity,
            'price': price,
        })
        total_price += price * quantity
        city = product.city

    context = {
        'cart_products': cart_products,
        'total_price': total_price,
        'city': city,
    }
    return render(request, "checkout.html", context)


def send_message_to_customer(request, customer, order_items, order):
    subject = "Формула SPA - новый заказ"
    recepient = customer.email
    msg_html = render_to_string('message.html', {
        'firstname': customer.firstname,
        'lastname': customer.lastname,
        'comment': order.comment,
        'is_digital': order.is_digital,
        'order_items': order_items,
        'order': order})

    send_mail(subject, '', EMAIL_HOST_USER, [recepient], html_message=msg_html, fail_silently=False)


def send_message_to_spa_center(request, customer, order_items, order):
    spa_subject = "Новый заказ"
    spa_recepient = "formulaspa11@mail.ru"
    spa_msg_html = render_to_string('message-to-admin.html', {
        'firstname': customer.firstname,
        'lastname': customer.lastname,
        'comment': order.comment,
        'is_digital': order.is_digital,
        'order_items': order_items,
        'order': order,
        'email': customer.email,
        'phonenumber': customer.phonenumber,
        'address': customer.address
    })

    send_mail(spa_subject, '', EMAIL_HOST_USER, [spa_recepient], html_message=spa_msg_html, fail_silently=False)


def checkout_user_data(request):
    try:
        cart = request.session['cart']
    except KeyError:
        return redirect(reverse('index'))

    if request.method == 'POST':
        firstname = request.POST.get('firstName')
        lastname = request.POST.get('lastName')
        email = request.POST.get('userEmail')
        phonenumber = request.POST.get('tel')
        address = request.POST.get('address')
        is_digital = request.POST.get('scales')
        comment = request.POST.get('comment')
        delivery = request.POST.get('delivery')

        customer, created = Customer.objects.get_or_create(
            firstname=firstname,
            lastname=lastname,
            phonenumber=phonenumber,
            email=email,
            address=address,
        )

        if is_digital:
            is_digital = True
        else:
            is_digital = False
        order = Order.objects.create(
            registrated_at=datetime.now(),
            comment=comment,
            is_digital=is_digital,
            customer=customer,
            sber_id='',
        )
        order_items = []
        for product_id in cart:
            product = get_object_or_404(Product, pk=product_id)
            order_item = OrderItem(
                product=product,
                order=order,
                quantity=cart[product_id]
            )
            order_items.append(order_item)

            order_item.save()

        if request.method == 'POST':
            url = 'https://3dsec.sberbank.ru/payment/rest/register.do'
            token = env('SBER_TOKEN')
            if delivery and int(order.cart_total) < 3000:
                payload = {
                    'token': token,
                    'orderNumber': order.id,
                    'returnUrl': 'http://104.248.23.29:8000/payment',
                    'amount': int(str(order.cart_total) + '00') + 300,
                }
            else:
                payload = {
                    'token': token,
                    'orderNumber': order.id,
                    'returnUrl': 'http://104.248.23.29:8000/payment',
                    'amount': int(str(order.cart_total) + '00'),
                }
            response = requests.post(url, data=payload)
            print(response.json())
            sber_id = response.json()['orderId']
            order.sber_id = sber_id
            order.save()
            form_url = response.json()['formUrl']
            return redirect(form_url)


def payment(request):
    url = 'https://3dsec.sberbank.ru/payment/rest/getOrderStatusExtended.do'
    my_payload = {
        'token': env('SBER_TOKEN'),
        'orderId': request.GET.get('orderId'),
    }
    order = get_object_or_404(Order, sber_id=my_payload['orderId'])
    customer = order.customer
    order_items = OrderItem.objects.filter(order=order)

    response = requests.post(url, data=my_payload)
    order_status = response.json()['orderStatus']
    if order_status == 2:
        print('SUCCESS! Send message!')
        order.is_complete = True
        send_message_to_customer(request, customer, order_items, order)
        send_message_to_spa_center(request, customer, order_items, order)
    else:
        print('NO!')
    return render(request, "payment.html")