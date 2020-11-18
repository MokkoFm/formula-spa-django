from django.urls import path
from spaweb import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('login/', views.login, name="login"),
    path('product/<slug:slug>', views.product_detail, name="product-detail"),
    path('category/<slug:slug>', views.product_listing, name="category"),
    path('register/', views.register, name="register"),
    path('cart/', views.cart, name="cart"),
    path('standalone/', views.standalone, name="standalone")
]
