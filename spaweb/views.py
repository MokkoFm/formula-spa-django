from django.shortcuts import render, redirect, reverse
from django.shortcuts import get_object_or_404
from spaweb.models import Product, ProductCategory, Topic

from spaweb.cart import add_to_cart


def index(request):
    new_products = Product.objects.filter(is_new=True)
    bestsellers = Product.objects.filter(is_bestseller=True)
    topics = Topic.objects.all()

    context = {
        "new_products": new_products,
        "bestsellers": bestsellers,
        "topics": topics,
    }
    return render(request, "index.html", context)


def contact(request):
    return render(request, "contact.html")


def login(request):
    return render(request, "login.html")


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    category = product.category

    if request.method == 'GET':
        context = {
            'product': get_object_or_404(Product, slug=slug),
            'category': category,
        }
        return render(request, "product-detail.html", context)

    if request.method == 'POST':
        add_to_cart(request)
        return redirect('product-detail', slug=product.slug)


def product_listing(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    categories = ProductCategory.objects.all()
    topics = Topic.objects.all()
    if request.method == "POST":
        minprice = request.POST.get('minprice')
        maxprice = request.POST.get('maxprice')
        if minprice or maxprice:
            products_by_category = Product.objects.filter(
                category=category, price__range=(minprice, maxprice))
        else:
            minprice = "0"
            maxprice = "10000"
            products_by_category = Product.objects.filter(
                category=category, price__range=(minprice, maxprice))
    else:
        products_by_category = Product.objects.filter(category=category)

    context = {
        'products_by_category': products_by_category,
        'category_slug': slug,
        'categories': categories,
        'topics': topics
    }
    return render(request, 'category.html', context)


def register(request):
    return render(request, 'register.html')


def cart(request):
    cart = request.session['cart']
    cart_products = []
    for key in cart:
        product = get_object_or_404(Product, pk=key)
        total_price = product.price * cart[key]
        
        cart_products.append({
            'product': product,
            'quantity': cart[key],
            'total_price': total_price,
        })

    context = {
        'cart_products': cart_products,
    }
    return render(request, "shop-cart.html", context)


def remove_cart_item(request, pk):
    cart = request.session['cart']
    cart.pop(pk, None)
    request.session['cart'] = cart
    return redirect(reverse('cart'))


def promo(request):
    return render(request, "promo.html")


def declarations(request):
    return render(request, "declarations.html")


def faq(request):
    return render(request, "faq.html")