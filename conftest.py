import os

import pytest
from apps.users.factories import UserFactory
from playwright.sync_api import Page

os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def user(db, client):
    _user = UserFactory.create()
    client.force_login(_user)
    return _user


@pytest.fixture
def e2e_user(live_server, db, page: Page):
    _user = UserFactory.create()
    page.goto(live_server.url + "/accounts/login/")
    page.get_by_label("Email address").fill(_user.email)
    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Log in").click()
    return _user
