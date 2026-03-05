
from .views import register
from django.urls import path


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]