from django.urls import path

from .views import signup

app_name = 'users'

urlpatterns = [
    path('auth/signup/', signup, name='signup')
]
