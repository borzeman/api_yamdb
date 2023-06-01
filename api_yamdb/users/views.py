from django.core.mail import send_mail
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import CustomUser
from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if (
        CustomUser.objects.filter(email=request.data.get('email')) and
        CustomUser.objects.filter(username=request.data.get('username'))):
        send_mail(
            'Test Title.',
            'Test message.',
            'test@gmail.com',
            [request.data.get('email')],
            fail_silently=False
        )
    if serializer.is_valid():
        print(12123)
        serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
