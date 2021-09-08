from django.urls import path

from apps.users.views import DeleteUserView, EmailLoginView, UserUpdateView, logout_view

app_name = "users"

urlpatterns = [
    path("login/", EmailLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
    path("accounts/update/", UserUpdateView.as_view(), name="user_update"),
    path("accounts/delete/", DeleteUserView.as_view(), name="user_delete"),
]
