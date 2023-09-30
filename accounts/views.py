from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from django.http import HttpRequest
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.views import (
    LoginView as BaseLoginView, 
    LogoutView as BaseLogoutView
)

from backend.utils import render_htmx
from backend.mixins import HTMXTemplateMixin
from products.models import Product

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
        self.render_to_response
        auth_login(self.request, form.get_user())
        # Now I should redirect the user to the index but all the solutions available will required reloading the page
        # So The only way to do this is to render the index.html template and pass the context again but I still want
        # to change this way to something better
        path = self.get_success_url()
        products = Product.objects.all().order_by('-created_at')[:6]
        template_name = 'core/index.html'
        context = {
            'products':products
        }
        headers = {
            'HX-Push-Url':path,
            'HX-Retarget':'body'
        }
        response = self.response_class(
            request=self.request,
            template=[template_name],
            context=context,
            headers=headers,
        )
        return response


class LogoutView(BaseLogoutView):
    template_name = 'registration/logout.html'

    def get(self, request, *args, **kwargs):
        """ In django 4 I have to implement this method otherwise django will logout users when they issue a GET request
            but please note that this will be removed in django 5 and django will not allow users to logout in GET since it's
            not secure
        """
        context = self.get_context_data()
        return self.render_to_response(context)
