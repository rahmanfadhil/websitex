from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import gettext_lazy as _

from apps.core.utils import compress_image
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
    def clean_avatar(self):
        data = self.cleaned_data["avatar"]
        if data:
            return compress_image(data, (256, 256))
        return data

    class Meta:
        model = User
        fields = ("email", "username", "full_name", "avatar")
        widgets = {"avatar": CustomClearableFileInput}


class SignupForm(forms.ModelForm):
    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_("A user with this email already exists."))
        return email

    class Meta:
        model = User
        fields = ("full_name", "email")


class LoginForm(forms.Form):
    email = forms.EmailField()
