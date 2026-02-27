from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)


