import os
import time

import jwt
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import ConfirmCode, CustomUser
from .permissions import AdminOnly
from .serializers import CustomUserSerializer, TokenSerializer, UserSerializer

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')


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
