from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.forms import CustomUserChangeForm, CustomUserCreationForm
from apps.users.models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ["email", "username"]


admin.site.register(User, CustomUserAdmin)
