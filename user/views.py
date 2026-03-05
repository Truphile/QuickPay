from django.shortcuts import render

from services.onboarding_service import create_user_and_wallet
from .serializers import UserSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user, wallet = create_user_and_wallet(serializer.validated_data)
    return Response({"message": "Registration successful"}, status=status.HTTP_201_CREATED )


@api_view(['POST'])
def login(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    return Response({"message": "Login successful", "data": serializer.validated_data}, status=status.HTTP_200_OK)


