from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail

from .tokens import account_activation_token_generator


def send_activation_token(request, user):
    subject = "Activate your account"

    domain = get_current_site(request).domain
    name = f'{user.first_name} {user.last_name}'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token_generator.make_token(user)
    protocol = 'https' if request.is_secure() else 'http'
    message = render_to_string(
        'registration/activation_email_template.html',{
            'domain':domain,
            'email':user.email,
            'name':name,
            'uid':uid,
            'token':token,
            'protocol':protocol
        }
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[user.email]
        
    )


