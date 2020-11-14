from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact', views.contact, name="contact"),
    path('login', views.login, name="login"),
    path('product/<slug:slug>', views.product_detail, name="product-detail"),
]
