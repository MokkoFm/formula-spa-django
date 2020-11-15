from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def login(request):
    return render(request, "login.html")


def product_detail(request):
    return render(request, "product-detail.html")


def product_listing(request):
    return render(request, 'product-listing.html')


def register(request):
    return render(request, 'register.html')


def cart(request):
    return render(request, "shop-cart.html")


def standalone(request):
    return render(request, "standalone.html")
