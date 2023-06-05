from django.urls import include, path
from  rest_framework import routers

from .views import create_token, signup, UserViewSet

app_name = 'users'
router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', create_token, name='get_token'),
    path('', include(router.urls))
]
