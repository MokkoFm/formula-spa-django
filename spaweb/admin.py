from django.contrib import admin
from spaweb.models import Customer, ProductCategory, City
from spaweb.models import Product, Order, ShippingAddress, OrderItem


admin.site.register(Customer)
admin.site.register(ProductCategory)
admin.site.register(City)
admin.site.register(Product)
admin.site.register(ShippingAddress)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'customer', 'registrated_at', 'comment',
        'is_complete', 'is_digital', 'payment_method',
    ]
    inlines = [OrderItemInline]
