from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('confirm_email/', views.confirm_email, name='confirm_email'),
    path('activate_email/<uidb64>/<token>/', views.activate_email, name='activate_email'),
    path('change_password/', views.PasswordChangeView.as_view(), name='password_chnage')
]
