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
    path('quantity/<str:pk>', views.change_item_quantity, name="change_quantity"),
    path('search/', views.search, name="search"),
    path('checkout/', views.checkout, name="checkout"),
    path('topic/<slug:slug>/', views.get_topic_listing, name="topic"),
]
