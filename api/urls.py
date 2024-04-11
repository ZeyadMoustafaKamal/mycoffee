from django.urls import include, path

urlpatterns = [
    path('accounts/', include('api.accounts.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
