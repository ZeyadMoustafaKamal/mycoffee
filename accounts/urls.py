from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('confirm_email/', views.confirm_email, name='confirm_email'),
    path('activate_email/<uidb64>/<token>/', views.activate_email, name='activate_email'),
    path('change_password/', views.PasswordChangeView.as_view(), name='password_chnage'),
    path('reset_password/', views.PasswordResetView.as_view(), name='password_reset'),
    path(
        'confirm_reset_password/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path('profile/', views.UserUpdateView.as_view(), name='profile')
]
