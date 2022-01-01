from django.urls import path

from apps.users.views import delete_user, password_reset, signup, update_user

app_name = "users"

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("accounts/update/", update_user, name="update_user"),
    path("accounts/delete/", delete_user, name="delete_user"),
    path("accounts/password_reset/", password_reset, name="password_reset"),
]
