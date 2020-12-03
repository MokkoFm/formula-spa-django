from django.contrib import admin
from spaweb.models import Customer, ProductCategory, City
from spaweb.models import Product, Order, OrderItem
from spaweb.models import BusinessDirection, Topic


admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(City)
admin.site.register(BusinessDirection)
admin.site.register(Topic)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    list_display = ['product', 'quantity', 'order_cost']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['registrated_at','is_complete', 'is_digital', 'payment_method']
    inlines = [OrderItemInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_filter = ['category']