from django.db.models.signals import post_save
from django.dispatch import receiver

from orders.models import Cart

from .models import User


@receiver(post_save, sender=User)
def create_user_handler(instance, created, *args, **kwargs):
    if created:
        # Create a Cart instnace for future use
        Cart.objects.create(user=instance)
