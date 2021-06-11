from allauth.account.forms import LoginForm, SignupForm
from crispy_forms.layout import Submit
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
        fields = ("full_name", "email", "username")


class CustomSignupForm(SignupForm, CrispyFormMixin):
    def get_submit_button(self) -> Submit:
        return Submit("signup", "Sign up", css_class="mt-4 btn-lg d-block w-100")


class CustomLoginForm(LoginForm, CrispyFormMixin):
    def get_submit_button(self) -> Submit:
        return Submit("login", "Login", css_class="mt-4 btn-lg d-block w-100")
