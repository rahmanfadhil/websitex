from django.urls import path

from apps.users.views import DeleteUserView, UserUpdateView, WellKnownChangePasswordView

app_name = "users"

urlpatterns = [
    path(
        ".well-known/change-password/",
        WellKnownChangePasswordView.as_view(),
        name="well_known_change_password",
    ),
    path("accounts/update/", UserUpdateView.as_view(), name="user_update"),
    path("accounts/delete/", DeleteUserView.as_view(), name="user_delete"),
]
