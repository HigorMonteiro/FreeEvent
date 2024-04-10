from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserAdminCreationForm, UserAdminForm
from .models import User


class UserAdmin(BaseUserAdmin):

    add_form = UserAdminCreationForm
    add_fieldsets = (
        (None, {"fields": ("username", "email", "password1", "password2")}),
    )
    form = UserAdminForm
    fieldsets = (
        (None, {"fields": ("username", "email")}),
        ("Informações Básicas", {"fields": ("name", "last_login")}),
        (
            "Permissões",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    list_display = [
        "username",
        "name",
        "email",
        "is_active",
        "is_staff",
        "date_joined",
    ]
    search_fields = ["username", "name", "email"]
    filter_horizontal = ["groups", "user_permissions", "is_active", "is_staff"]

admin.site.register(User, UserAdmin)
