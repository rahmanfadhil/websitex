from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView

from apps.users.forms import UserUpdateForm
from apps.users.models import User


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateForm

    def get_object(self, queryset=None) -> User:
        return self.request.user
