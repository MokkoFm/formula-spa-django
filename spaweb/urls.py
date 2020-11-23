from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('product/<slug:slug>/', views.product_detail, name="product-detail"),
    path('category/<slug:slug>', views.product_listing, name="category"),
    path('cart/', views.cart, name="cart"),
    path('promo/', views.promo, name="promo"),
    path('declarations/', views.declarations, name="declarations"),
    path('faq/', views.faq, name="faq"),
    path('remove/<str:pk>', views.remove_cart_item, name="remove_item"),
]
