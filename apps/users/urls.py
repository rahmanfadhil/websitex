from django.urls import path

from apps.users.views import DeleteUserView, UserUpdateAvatarView, UserUpdateView

app_name = "users"

urlpatterns = [
    path("account/update/", UserUpdateView.as_view(), name="user_update"),
    path("update-avatar/", UserUpdateAvatarView.as_view(), name="update_avatar"),
    path("delete-user/", DeleteUserView.as_view(), name="user_delete"),
]
