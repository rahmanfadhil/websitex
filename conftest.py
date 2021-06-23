import pytest

from apps.users.factories import UserFactory


@pytest.fixture
def user(db, client):
    _user = UserFactory.create()
    client.force_login(_user)
    return _user
