from django.contrib.auth import authenticate
from apps.users.factories import UserFactory


def test_email_backend_success(db):
    user = UserFactory.create()
    user = authenticate(username=user.email, password="12345")
    assert user == user


def test_email_backend_fail(db):
    user = UserFactory.create()
    user = authenticate(username=user.email, password="wrong")
    assert user is None
