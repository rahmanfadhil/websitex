from io import BytesIO

from django.contrib.messages import get_messages
from django.core.files import File
from django.test import Client
from PIL import Image
from pytest_django.asserts import assertRedirects

from apps.users.models import User


def test_remove_avatar(client: Client, user: User):
    response = client.post("/update-avatar/", {"avatar-clear": "on"})
    assertRedirects(response, "/account/update/")

    user.refresh_from_db()
    assert not user.avatar

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].message == "Successfully updated your profile picture!"


def test_change_avatar(client: Client, user: User):
    user.avatar = None
    user.save()

    content = BytesIO()
    Image.new("RGB", (512, 512), "green").save(content, "JPEG")
    content.seek(0)
    file = File(content, "photo.jpg")

    response = client.post("/update-avatar/", {"avatar": file})
    assertRedirects(response, "/account/update/")

    user.refresh_from_db()
    assert user.avatar
    assert user.avatar.width == 256
    assert user.avatar.height == 256

    messages = list(get_messages(response.wsgi_request))
    assert len(messages) == 1
    assert messages[0].message == "Successfully updated your profile picture!"


def test_delete_user(client: Client, user: User):
    response = client.post("/account/delete/")
    assertRedirects(response, "/")
    assert not User.objects.exists()
