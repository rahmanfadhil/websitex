from django.contrib.auth import authenticate, get_user
from pytest_django.asserts import assertRedirects

from apps.users.factories import UserFactory
from apps.users.models import User


def test_email_backend_success(db):
    user = UserFactory.create()
    user = authenticate(username=user.email, password="12345")
    assert user == user


def test_email_backend_fail(db):
    user = UserFactory.create()
    user = authenticate(username=user.email, password="wrong")
    assert user is None


def test_delete_user(client, user):
    response = client.post("/accounts/delete/")
    assertRedirects(response, "/")
    assert not User.objects.exists()


def test_login_success(db, client):
    user = UserFactory.create()
    data = {"username": user.email, "password": "12345"}
    response = client.post("/accounts/login/", data)
    assertRedirects(response, "/")
    assert get_user(client) == user


def test_login_fail(db, client):
    user = UserFactory.create()
    data = {"username": user.email, "password": "wrong"}
    response = client.post("/accounts/login/", data)
    assert response.status_code == 200
