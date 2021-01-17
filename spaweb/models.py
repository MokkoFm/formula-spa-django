from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from tinymce.models import HTMLField


class BusinessDirection(models.Model):
    title = models.CharField('название', max_length=50)
    slug = models.SlugField(null=True, unique=True)

    class Meta:
        verbose_name_plural = "направления"

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField('название', max_length=50)
    business_direction = models.ForeignKey(
        BusinessDirection, on_delete=models.CASCADE,
        related_name='topics', null=True)
    slug = models.SlugField(null=True, unique=True)

    class Meta:
        verbose_name_plural = "группы категорий"

    def __str__(self):
        return self.title


class ProductCategory(models.Model):
    name = models.CharField('название', max_length=50)
    topic = models.ForeignKey(
        Topic, on_delete=models.CASCADE,
        related_name='products_categories', null=True)
    slug = models.SlugField(null=True, unique=True)

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

    @property
    def absolute_url(self):
        return reverse('product-listing', kwargs={'slug': self.slug})


class Product(models.Model):
    name = models.CharField('название', max_length=50)
    description = HTMLField(verbose_name='описание', blank=True)
    category = models.ForeignKey(
        ProductCategory, verbose_name='категория', null=True,
        related_name='category_products', on_delete=models.SET_NULL)
    city = models.ForeignKey(
        City, verbose_name='город', related_name='city_products', on_delete=models.CASCADE, null=True)
    price = models.DecimalField('цена', max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="images", verbose_name="фото товара")
    duration = models.CharField(
        verbose_name='Продолжительность', max_length=50, blank=True)
    is_bestseller = models.BooleanField(
        default=False, db_index=True, verbose_name="популярные товары")
    is_new = models.BooleanField(
        default=False, db_index=True, verbose_name="новый товар")
    slug = models.SlugField(null=True, unique=True)

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


class Customer(models.Model):
    firstname = models.CharField(max_length=50, verbose_name="имя")
    lastname = models.CharField(max_length=50, verbose_name="фамилия")
    phonenumber = models.CharField(
        max_length=20, blank=True, verbose_name="телефон")
    email = models.CharField(
        max_length=100, blank=True, verbose_name="эл. почта")
    address = models.TextField(verbose_name="адрес для доставки", null=True)

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"


class Order(models.Model):
    PAYMENT_METHOD = [
        ('Cash', 'Наличными'),
        ('Card', 'По карте'),
    ]

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
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders', verbose_name='Покупатель', null=True)
    sber_id = models.TextField(verbose_name='ID заказа в сбербанке', blank=True, null=True)

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
