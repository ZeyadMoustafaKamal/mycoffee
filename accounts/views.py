from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.http import HttpRequest
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.views import (
    LoginView as BaseLoginView, 
    LogoutView as BaseLogoutView
)

from core.utils import render_htmx
from core.mixins import HTMXTemplateMixin
from core.utils import HTMXRedirect

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
            return HTMXRedirect(reverse('index'))
    context = {'form':form}
    return render_htmx(
        request, 
        'registration/signup.html', 
        'registration/parts/_signup.html', 
        context
    )


class LoginView(HTMXTemplateMixin, BaseLoginView):
    form_class = AuthenticationForm
    htmx_template = 'registration/parts/_login.html'
    def post(self, request, *args, **kwargs):
        if not 'remember' in request.POST:
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
        """ In django 4 I have to implement this method otherwise django will logout users when they issue a GET request
            but please note that this will be removed in django 5 and django will not allow users to logout in GET since it's
            not secure
        """
        context = self.get_context_data()
        return self.render_to_response(context)
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs) # This will be useful if django added some functionality to this view
        return HTMXRedirect(self.success_url)
        
