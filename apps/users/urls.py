from django.urls import path

from apps.users.views import delete_user, logout, login, update_user, delete_user

app_name = "users"

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("accounts/update/", update_user, name="update_user"),
    path("accounts/delete/", delete_user, name="delete_user"),
]
