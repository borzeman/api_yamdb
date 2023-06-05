from django.urls import include, path
from rest_framework import routers
from .views import (
    create_token,
    signup,
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
    UserViewSet,
)

app_name = 'api'
router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')

review_router = routers.DefaultRouter()
review_router.register(r'reviews', ReviewViewSet, basename='reviews')

comment_router = routers.DefaultRouter()
comment_router.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('auth/signup/', signup, name='signup'),
    path('auth/token/', create_token, name='get_token'),
    path('', include(router.urls)),
    path('titles/<int:title_id>/', include(review_router.urls)),
    path('titles/<int:title_id>/', include(comment_router.urls)),
]