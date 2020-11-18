from django.shortcuts import render
from django.shortcuts import get_object_or_404
from spaweb.models import Product, ProductCategory, Topic


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
    context = {
        "product": get_object_or_404(Product, slug=slug)
    }
    return render(request, "product-detail.html", context)


def product_listing(request, slug):
    category = get_object_or_404(ProductCategory, slug=slug)
    if request.method == "POST":
        minprice = request.POST.get('minprice')
        maxprice = request.POST.get('maxprice')
        products_by_category = Product.objects.filter(category=category, price__range=(minprice, maxprice))
    else:
        products_by_category = Product.objects.filter(category=category)

    context = {
        'products_by_category': products_by_category,
    }
    return render(request, 'category.html', context)


def register(request):
    return render(request, 'register.html')


def cart(request):
    return render(request, "shop-cart.html")


def promo(request):
    return render(request, "promo.html")


def declarations(request):
    return render(request, "declarations.html")