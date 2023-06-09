import jwt
import time
import os

from dotenv import load_dotenv
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend, FilterSet
import django_filters
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import filters, mixins, serializers, status, viewsets

from users.models import CustomUser, ConfirmCode
from artworks.models import Category, Genre, Title
from reviews.models import Comment, Review
from .permissions import AdminOnly, IsOwnerOrReadOnly, ReadOnly, IsAuthorAdminModerator, IsModerator
from .serializers import (
    CustomUserSerializer,
    TokenSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
    CommentSerializer,
)


load_dotenv()
# SECRET_KEY = os.getenv('SECRET_KEY')
SECRET_KEY = 'rjnfijrnfkslmf3f234'

def create_confirm_code(data: dict) -> None:
    dict_data = {
        'user': data.get('username'),
        'time': int(time.time())
    }
    confirmation_code = encode_data(dict_data)
    send_mail(
        'Test Title.',
        confirmation_code,
        'test@gmail.com',
        [data.get('email')],
        fail_silently=False
    )
    confirmation_code_dict = {'hash_code': confirmation_code}
    hash_summ_cc = encode_data(confirmation_code_dict)
    user = CustomUser.objects.get(username=data.get('username'))
    if ConfirmCode.objects.filter(user=user).exists():
        ConfirmCode.objects.get(user=user).delete()
    ConfirmCode.objects.create(
        user=user,
        confirmation_code=hash_summ_cc
    )


def encode_data(data: dict) -> str:
    encode_data = jwt.encode(
        payload=data, key=SECRET_KEY, algorithm='HS256')
    return encode_data


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {'access': str(refresh.access_token)}


@api_view(['POST'])
def signup(request):
    email = request.data.get('email')
    username = request.data.get('username')
    if username == 'me':
        return Response(
            'Username не может быть "me".',
            status=status.HTTP_400_BAD_REQUEST
        )
    if (CustomUser.objects.filter(
        email=email,
        username=username
    ).exists()):
        create_confirm_code(request.data)
        return Response(
            'Message was sent, check out you mail.',
            status=status.HTTP_200_OK)
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    create_confirm_code(serializer.data)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_token(request):
    serializer = TokenSerializer(data=request.data)
    if not serializer.is_valid():
        if serializer.data.get('username') is not None:
            return Response(
                'Username doesn\'t exist.',
                status=status.HTTP_404_NOT_FOUND
            )
        serializer.is_valid(raise_exception=True)
    user = serializer.validated_data.get('user')
    confirm_code = {
        'hash_code': serializer.validated_data.get('confirmation_code')}
    if ConfirmCode.objects.filter(
        user=user,
        confirmation_code=encode_data(confirm_code)
    ).exists():
        token = get_token_for_user(user)
        return Response(token, status=status.HTTP_200_OK)
    return Response('Something wrong.', status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()
    permission_classes = (AdminOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    search_fields = ('username',)
    lookup_field = 'username'

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        permission_classes=[IsAuthenticated,]
    )
    def me(self, request):
        user = get_object_or_404(CustomUser, username=self.request.user)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = CustomUserSerializer(
            user,
            data=request.data,
            context={'request': request},
            partial=True
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [ReadOnly|AdminOnly]
    #permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (filters.SearchFilter, )
    lookup_field = 'slug'
    search_fields = ('name',)

class GenreViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [ReadOnly|AdminOnly]
    #permission_classes = [AllowAny, ]
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    search_fields = ('name',)

class TitleFilter(FilterSet):
    genre = django_filters.CharFilter(field_name='genre__slug', lookup_expr='exact')
    category = django_filters.CharFilter(field_name='category__slug', lookup_expr='exact')
    class Meta:
        model = Title
        fields = {
            'name': ['exact', 'icontains'],
            'year': ['exact', 'gte', 'lte'],
        }

class TitleViewSet(viewsets.ModelViewSet):
    permission_classes = [ReadOnly|AdminOnly]
    #permission_classes = [AllowAny, ]
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorAdminModerator|ReadOnly|AdminOnly]

    def get_title(self):
        return get_object_or_404(
            Title,
            id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=self.get_title()
        )

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorAdminModerator|ReadOnly|AdminOnly]

    def get_review(self):
        return get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'),
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, review=self.get_review()
        )