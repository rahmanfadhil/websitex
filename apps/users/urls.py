from django.urls import path
from apps.users.views import UserUpdateView


app_name = "users"

urlpatterns = [
    path("user-update/", UserUpdateView.as_view(), name="user_update"),
]
