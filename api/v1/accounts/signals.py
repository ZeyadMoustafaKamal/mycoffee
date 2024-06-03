from django.contrib.sites.shortcuts import get_current_site
from django.dispatch import receiver
from djoser.signals import user_registered

from accounts.utils import send_activation_token


@receiver(user_registered)
def create_user_handler(user, request, *args, **kwargs):
    domain = get_current_site(request).domain
    protocol = 'https' if request.is_secure() else 'http'
    send_activation_token.delay(domain, protocol, user.pk)
