from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from apps.core.forms import CrispyFormMixin
from apps.users.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("email", "username")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("email", "username")


class UserUpdateForm(forms.ModelForm, CrispyFormMixin):
    class Meta:
        model = User
        fields = ("full_name", "username")
