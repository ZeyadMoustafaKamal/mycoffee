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
    readonly_fields = 'id', 'user', 'get_total', 'created_at'
    inlines = [OrderItemInline]
    ordering = ['-created_at']
    list_filter = ['status']

    def has_add_permission(self, request):
        """ Great right ??
        Now even superusers can't create new orders from the admin panel when it goes to production
        """
        return settings.DEBUG

    def has_delete_permission(self, request, obj=None):
        return settings.DEBUG

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(cart=None)
        return qs.select_related('user').prefetch_related('items')

    def get_object(self, request, object_id, from_field=None):
        return super().get_object(request, object_id, from_field)

    def get_total(self, obj):
        return obj.get_total
    get_total.short_description = 'Total price'

    def _changeform_view(self, request, object_id, form_url, extra_context):
        res = super()._changeform_view(request, object_id, form_url, extra_context)

        # print(res.context_data.get('errors').as_json())
        return res


admin.site.register(Order, OrderAdmin)
