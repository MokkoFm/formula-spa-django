from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact', views.contact, name="contact"),
    path('login', views.login, name="login"),
    path('product/<slug:slug>', views.product_detail, name="product-detail"),
    path('product-listing', views.product_listing, name="product-listing"),
    path('register', views.register, name="register"),
    path('cart', views.cart, name="cart"),
    path('standalone', views.standalone, name="standalone")
]
