from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .tokens import account_activation_token_generator

User = get_user_model()


@shared_task()
def send_activation_token(domain, protocol, user_pk):
    subject = "Activate your account"
    user = User.objects.get(pk=user_pk)

    name = f'{user.first_name} {user.last_name}'
    uid = urlsafe_base64_encode(force_bytes(user_pk))
    token = account_activation_token_generator.make_token(user)
    message = render_to_string(
        'registration/activation_email_template.html', {
            'domain': domain,
            'email': user.email,
            'name': name,
            'uid': uid,
            'token': token,
            'protocol': protocol
        }
    )
    send_mail(
        subject=subject,
        message=message,
        from_email=None,
        recipient_list=[user.email]
    )


def get_user_from_uidb64(uidb64):
    """ Used to get the user from the uid64 and the token
        which is in the confirmation url that will be sent to the user
    """
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        return None
    else:
        return user
