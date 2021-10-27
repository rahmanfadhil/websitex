from pytest_django.asserts import assertRedirects

from apps.users.models import User


def test_delete_user(client, user):
    response = client.post("/account/delete/")
    assertRedirects(response, "/")
    assert not User.objects.exists()
