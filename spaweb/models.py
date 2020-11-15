from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse


class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=20, blank=True)
    email = models.CharField(max_length=100, blank=True)
    user = models.OneToOneField(
        User, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField('название', max_length=50)

    class Meta:
        verbose_name = 'город'
        verbose_name_plural = 'города'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    description = models.TextField('описание')
    category = models.ManyToManyField(
        ProductCategory, verbose_name='категория',
        related_name='category_products')
    city = models.ManyToManyField(
        City, verbose_name='город', related_name='city_products')
    price = models.DecimalField('цена', max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="images", verbose_name="фото товара")
    ingredients = models.CharField(
        verbose_name='что включено', max_length=200, blank=True)
    slug = models.SlugField(null=True)

    def __str__(self):
        return self.name

    @property
    def absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})

    @property
    def image_url(self):
        try:
            url = self.image.url
        except AttributeError:
            url = ''
        return url

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'


class Order(models.Model):
    PAYMENT_METHOD = [
        ('Cash', 'Наличными'),
        ('Card', 'По карте'),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        related_name='orders', verbose_name="клиент")
    registrated_at = models.DateTimeField(
        default=timezone.now, verbose_name='дата регистрации')
    comment = models.TextField(verbose_name='комментарий', blank=True)
    is_digital = models.BooleanField(
        default=False, db_index=True, verbose_name="эл. сертификат")
    is_complete = models.BooleanField(
        default=False, db_index=True, verbose_name="статус")
    payment_method = models.CharField(
        max_length=4, choices=PAYMENT_METHOD,
        default='Неизвестно', verbose_name='способ оплаты')

    def __str__(self):
        return f" Order number - {self.id}"

    @property
    def cart_total(self):
        return sum([item.total for item in self.order_items.all()])

    @property
    def cart_items_amount(self):
        return sum([item.quantity for item in self.order_items.all()])

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE,
        related_name='product_items')
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='order_items')
    quantity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(25)],
        verbose_name='количество', default=0)

    def __str__(self):
        return f"{self.product}: {self.quantity}"

    @property
    def total(self):
        return self.product.price * self.quantity

    class Meta:
        verbose_name = "товар в заказе"
        verbose_name_plural = "товары в заказе"


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="address")
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="address")
    address = models.TextField(verbose_name="адрес для доставки")
    city = models.ForeignKey(
        City, on_delete=models.CASCADE,
        verbose_name='город доставки', related_name="address")

    def __str__(self):
        return self.address

    class Meta:
        verbose_name = "адрес доставки"
        verbose_name_plural = "адреса доставки"