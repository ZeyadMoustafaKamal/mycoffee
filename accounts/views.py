from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.views import (  # isort: split
    LoginView as BaseLoginView,
    LogoutView as BaseLogoutView,
    PasswordChangeView as BasePasswordChangeView,
    PasswordResetView as BasePasswordResetView,
    PasswordResetConfirmView as BasePasswordResetConfirmView
)
from django.forms.models import model_to_dict
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import UpdateView

from core.mixins import SuccessMessageMixin
from htmx.base import HTMXRedirect, render_htmx
from htmx.mixins import HTMXRedirectMixin, HTMXTemplateMixin

from .forms import AuthenticationForm, PasswordChangeForm, PasswordResetForm, UserCreationForm, UserUpdateForm
from .models import UserProfile
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
            send_activation_token.delay(request, user)
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
    SuccessMessageMixin,
    LoginRequiredMixin,
    BasePasswordChangeView
):
    template_name = 'registration/password_change.html'
    htmx_template = 'registration/parts/_password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('index')
    success_message = 'Your password changed successfully'
    login_url = reverse_lazy('login')


class PasswordResetView(
    HTMXTemplateMixin,
    HTMXRedirectMixin,
    BasePasswordResetView
):
    template_name = 'registration/password_reset.html'
    htmx_template = 'registration/parts/_password_reset.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('index')


class PasswordResetConfirmView(
    HTMXTemplateMixin,
    HTMXRedirectMixin,
    SuccessMessageMixin,
    BasePasswordResetConfirmView
):
    success_url = reverse_lazy('index')
    success_message = 'Your password changed successfully'


class UserUpdateView(
    HTMXTemplateMixin,
    HTMXRedirectMixin,
    SuccessMessageMixin,
    LoginRequiredMixin,
    UpdateView
):
    form_class = UserUpdateForm
    template_name = 'registration/user_update.html'
    htmx_template = 'registration/parts/_user_update.html'
    success_message = 'Your information updated successfully'
    success_url = reverse_lazy('profile')
    login_url = reverse_lazy('login')

    def get_initial(self):
        user_profile = UserProfile.objects.get(user=self.request.user)
        user_initial = model_to_dict(self.request.user, fields=['first_name', 'last_name'])
        profile_intial = model_to_dict(user_profile, exclude='favourites')
        initial_data = user_initial | profile_intial
        return initial_data

    def get_object(self, queryset=None):
        return self.request.user
