from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from apps.users.models import User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ("full_name", "username")

    def get_object(self, queryset=None) -> User:
        return self.request.user
