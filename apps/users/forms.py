from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _

from apps.core.utils import compress_image
from apps.core.widgets import CustomClearableFileInput
from apps.users.models import User


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


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("full_name", "email")
        widgets = {"full_name": forms.TextInput(attrs={"autofocus": True})}


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"autofocus": True}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )
    error_messages = {
        "invalid_credentials": _("Invalid email or password."),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request: HttpRequest, *args, **kwargs):
        self.request = request
        self.user = None
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(self.request, email=email, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    self.error_messages["invalid_credentials"],
                    code="invalid_credentials",
                )
            if not self.user.is_active:
                raise forms.ValidationError(
                    self.error_messages["inactive"],
                    code="inactive",
                )

        return self.cleaned_data

    def get_user(self) -> User:
        return self.user
