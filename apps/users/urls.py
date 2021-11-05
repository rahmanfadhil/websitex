from django.urls import path

from apps.users.views import delete_user, login, logout, signup, update_user

app_name = "users"

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("logout/", logout, name="logout"),
    path("account/update/", update_user, name="update_user"),
    path("account/delete/", delete_user, name="delete_user"),
]
