from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView, View
from django.views.generic.edit import FormView
from sesame.utils import get_query_string

from apps.core.utils import compress_image, send_html_email
from apps.users.forms import EmailLoginForm, UserUpdateForm
from apps.users.models import User


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("pages:home")


class EmailLoginView(SuccessMessageMixin, FormView):
    form_class = EmailLoginForm
    template_name = "users/login.html"
    success_url = reverse_lazy("pages:home")
    success_message = "Sent login link to your email!"

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        user, _ = User.objects.get_or_create(email=email)
        url = self.request.build_absolute_uri(self.success_url + get_query_string(user))
        send_html_email(
            request=self.request,
            subject="Login",
            email=user.email,
            template_name="emails/login.html",
            context={"url": url, "user": user},
        )
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("users:user_update")
    success_message = "Successfully updated your profile!"
    template_name = "users/user_update.html"

    def get_object(self, queryset=None) -> User:
        return self.request.user

    def form_valid(self, form):
        # Compress the avatar image if the file has changed.
        if "avatar" in form.changed_data and form.cleaned_data.get("avatar"):
            avatar = compress_image(form.cleaned_data["avatar"], (256, 256))
            form.instance.avatar = avatar
        return super().form_valid(form)


class DeleteUserView(LoginRequiredMixin, View):
    success_message = "Your account has been successfully deleted!"
    success_url = reverse_lazy("pages:home")

    def post(self, request):
        request.user.delete()
        messages.success(request, self.success_message)
        return redirect(self.success_url)
