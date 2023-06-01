from django.shortcuts import render
from rest_framework.decorators import api_view

from .serializers import UserSerializer

@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request)
