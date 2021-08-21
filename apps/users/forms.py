from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from apps.core.widgets import CustomClearableFileInput
from apps.users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "username")


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email", "username", "full_name", "avatar")
        widgets = {"avatar": CustomClearableFileInput}
