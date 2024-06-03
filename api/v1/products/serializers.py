from rest_framework import serializers

from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'
        extra_fields = 'is_favourite'

    def get_is_favourite(self, obj):
        request = self.context['request']
        if request.user.is_anonymous:
            return None
        return obj in request.user.profile.favourites.all()
