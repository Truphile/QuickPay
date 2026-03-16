from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from user.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
    (
        None, {
            'classes': ('wide',),
            "fields": ("username","usable_password", "password1", "password2", "first_name", "last_name", "email", "phone"),
        },
    ),
    )

