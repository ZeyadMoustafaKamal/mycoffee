from django.shortcuts import redirect
from django.http import HttpRequest
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login as auth_login
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.views import (
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView
)
from django.contrib import messages

from htmx.base import render_htmx, HTMXRedirect
from htmx.mixins import HTMXTemplateMixin

from .forms import UserCreationForm, AuthenticationForm
from .utils import send_activation_token
from .tokens import account_activation_token_generator

import threading  # TODO: Use celery instead of threading

User = get_user_model()


def signup(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            threading.Thread(target=send_activation_token, args=(request, user)).start()
            return HTMXRedirect(reverse('confirm_email'))
    context = {'form': form}
    return render_htmx(
        request,
        'registration/signup.html',
        'registration/parts/_signup.html',
        context
    )


def confirm_email(request):
    return render_htmx(
        request,
        'registration/confirm_email.html',
        'registration/parts/_confirm_email.html'
    )


def activate_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(force_str(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        messages.error(request, "This URL is invalid or expired please try again later !!")
        return redirect(reverse('index'))

    if request.method == 'POST':
        if account_activation_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, "This account is activated successfully you can login now !!")
            return HTMXRedirect(reverse('index'))
        else:
            messages.error(request, "This URL is invalid or expired please try again later !!")
    context = {}
    context['email'] = user.email
    return render_htmx(
        request,
        'registration/activation_email_confirm.html',
        'registration/parts/_activation_email_confirm.html',
        context
    )


class LoginView(HTMXTemplateMixin, BaseLoginView):
    form_class = AuthenticationForm
    htmx_template = 'registration/parts/_login.html'

    def post(self, request, *args, **kwargs):
        if 'remember' not in request.POST:
            request.session.set_expiry(0)
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        path = self.get_success_url()
        return HTMXRedirect(path)


class LogoutView(HTMXTemplateMixin, BaseLogoutView):
    template_name = 'registration/logout.html'
    htmx_template = 'registration/parts/_logout.html'
    success_url = reverse_lazy('index')

    def get(self, request, *args, **kwargs):
        """ In django 4 I have to implement this method otherwise django will logout users when they issue a GET
            request but please note that this will be removed in django 5 and django will not allow users to logout
            in GET since it's not secure
        """
        context = self.get_context_data()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        # This will be useful if django added some functionality to this view
        super().post(request, *args, **kwargs)
        return HTMXRedirect(self.success_url)
