
from .views import register, login
from django.urls import path


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
]