import threading  # TODO: Use celery instead of threading

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.auth.views import PasswordChangeView as BasePasswordChangeView
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from htmx.base import HTMXRedirect, render_htmx
from htmx.mixins import HTMXRedirectMixin, HTMXTemplateMixin

from .forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from .utils import get_user_from_uidb64, send_activation_token

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
    user = get_user_from_uidb64(uidb64)
    if user is None:
        messages.error(request, "This URL is invalid or expired please try again later !!")
        return redirect(reverse('index'))
    if request.method == 'POST':
        if user.activate_from_token(token):
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


class LoginView(
    HTMXTemplateMixin,
    HTMXRedirectMixin,
    BaseLoginView
):
    form_class = AuthenticationForm
    htmx_template = 'registration/parts/_login.html'

    def post(self, request, *args, **kwargs):
        if 'remember' not in request.POST:
            request.session.set_expiry(0)
        return super().post(request, *args, **kwargs)


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


class PasswordChangeView(
    HTMXTemplateMixin,
    HTMXRedirectMixin,
    BasePasswordChangeView
):
    template_name = 'registration/password_change.html'
    htmx_template = 'registration/parts/_password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        messages.success(self.request, 'Your password changed successfully')
        return super().form_valid(form)
