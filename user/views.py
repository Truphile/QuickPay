from django.shortcuts import render
from .serializers import UserSerializer
# Create your views here.

def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

