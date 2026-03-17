from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


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
    def has_delete_permission(self, request, obj=None):
        if obj and obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

