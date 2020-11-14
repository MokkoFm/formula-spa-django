from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def contact(request):
    return render(request, "contact.html")


def login(request):
    return render(request, "login.html")


def product_detail(request):
    return render(request, "product-detail.html")
