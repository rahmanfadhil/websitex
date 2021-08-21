from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View
from django.views.generic.base import RedirectView

from apps.core.utils import compress_image
from apps.users.forms import UserUpdateForm
from apps.users.models import User


class WellKnownChangePasswordView(RedirectView):
    permanent = False
    pattern_name = "account_change_password"


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
