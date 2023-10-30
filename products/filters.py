import django_filters
from django.db.models import Q

from .models import Product


class ProductFilter(django_filters.FilterSet):
    case_sensitive = django_filters.BooleanFilter(method='filter_case_sensitive', label='Case sensitive')

    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'description': ['icontains'],
            'price': ['gt', 'lt']
        }

    def filter_case_sensitive(self, queryset, name, value):
        if value:
            return queryset.filter(
                name__exact=self.data.get('name'),
                description__exact=self.data.get('description')
            )
        return queryset

    def filter_queryset(self, queryset):
        qs = super().filter_queryset(queryset)
        # Assume that this is not from the advanced search page
        if 'price__gt' not in self.request.GET and 'price__lt' not in self.request.GET:
            name = self.request.GET.get('name__icontains')
            description = self.request.GET.get('description__icontains')
            qs = queryset.filter(Q(name__icontains=name) | Q(description__icontains=description))
        return qs
