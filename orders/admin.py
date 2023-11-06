from django.conf import settings
from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.StackedInline):
    model = OrderItem
    exclude = 'price', 'discounted_price'
    readonly_fields = [
        'order',
        'product',
        'get_price',
        'quantity',
        'city',
        'state',
        'zip_code',
        'address1',
        'address2',
    ]
    can_delete = False

    def get_price(self, obj):
        return obj.get_price
    get_price.short_description = 'Price'

    def get_max_num(self, request, obj, **kwargs):
        """ Means that the admin can't add more OrderItems to the Order instance """
        if obj:
            return len(obj.items.all())
        return super().get_max_num(request, obj, **kwargs)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = 'user', 'created_at'
    inlines = [OrderItemInline]

    def has_add_permission(self, request):
        """ Great right ??
        Now even the superusers can't create new orders from the admin panel when it goes to production
        """
        return settings.DEBUG


admin.site.register(Order, OrderAdmin)
