from django.urls import path

from .views import create_token, signup

app_name = 'users'

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', create_token, name='get_token'),
]
