from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('contact/', views.contact, name="contact"),
    path('product/<slug:slug>/', views.product_detail, name="product-detail"),
    path('category/<slug:slug>', views.product_listing, name="category"),
    path('cart/', views.cart, name="cart"),
    path('add_to_cart//<slug:slug>', views.add_to_cart, name="add_to_cart"),
    path('promo/', views.promo, name="promo"),
    path('declarations/', views.declarations, name="declarations"),
    path('security/', views.security, name="security"),
    path('faq/', views.faq, name="faq"),
    path('massage-course/', views.massage_course, name="massage_course"),
    path('remove/<str:pk>', views.remove_cart_item, name="remove_item"),
    path('quantity/<str:pk>', views.change_item_quantity, name="change_quantity"),
    path('search/', views.search, name="search"),
    path('checkout/', views.checkout, name="checkout"),
    path('checkout_data/', views.checkout_user_data, name="checkout_data"),
    path('topic/<slug:slug>/', views.get_topic_listing, name="topic"),
    path('payment', views.payment, name="payment"),
    path('calc-sauna', views.calc_sauna, name="sauna"),
    path('calc-hamam', views.calc_hamam, name="hamam"),
    path('calc-bochka-dlya-odnogo', views.calc_bochka_odin, name="bochka_odin"),
    path('calc-bochka-dlya-dvoih', views.calc_bochka_dva, name="bochka_dva"),
    path('calc-capsula', views.calc_capsula, name="capsula")
]
