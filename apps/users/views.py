from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, View

from apps.core.utils import compress_image
from apps.users.forms import UserUpdateForm
from apps.users.models import User


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    success_url = reverse_lazy("users:user_update")
    success_message = "Successfully updated your profile!"

    def get_object(self, queryset=None) -> User:
        return self.request.user


class UserUpdateAvatarView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ("avatar",)
    success_url = reverse_lazy("users:user_update")
    success_message = "Successfully updated your profile picture!"

    def get_object(self, queryset=None) -> User:
        return self.request.user

    def form_valid(self, form):
        if avatar := form.cleaned_data["avatar"]:
            form.instance.avatar = compress_image(avatar, (256, 256))
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = [item for sublist in form.errors.values() for item in sublist]
        message = "Failed to upload your image: {}".format(errors[0])
        messages.error(self.request, message)
        return super().form_invalid(form)


class DeleteUserView(LoginRequiredMixin, View):
    success_message = "Your account has been successfully deleted!"
    success_url = reverse_lazy("pages:home")

    def post(self, request):
        request.user.delete()
        messages.success(request, self.success_message)
        return redirect(self.success_url)
