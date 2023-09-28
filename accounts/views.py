from django.shortcuts import redirect
from django.http import HttpRequest
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView

from backend.utils import render_htmx
from backend.mixins import HTMXTemplateMixin

from .forms import UserCreationForm, AuthenticationForm

User = get_user_model()

def signup(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect('index')
    form = UserCreationForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
    context = {}
    context['form'] = form
    return render_htmx(request, 'registration/signup.html', 'registration/parts/_signup.html', context)


class LoginView(HTMXTemplateMixin, BaseLoginView):
    form_class = AuthenticationForm
    htmx_template = 'registration/parts/_login.html'
    def post(self, request, *args, **kwargs):
        if not 'remember' in request.POST:
            request.session.set_expiry(0)
        return super().post(request, *args, **kwargs)


class LogoutView(BaseLogoutView):
    template_name = 'registration/logout.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return self.render_to_response(context)
