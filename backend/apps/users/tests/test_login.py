from apps.users.factories import UserFactory
from playwright.sync_api import Page, expect


def test_login_success(live_server, db, page: Page):
    user = UserFactory.create()
    page.goto(live_server.url + "/accounts/login/")
    page.get_by_label("Email address").fill(user.email)
    page.get_by_label("Password").fill("12345")
    page.get_by_role("button", name="Log in").click()

    # Expect to be redirected to the home page.
    expect(page).to_have_url(live_server.url + "/")
    expect(page).to_have_title("WebsiteX")


def test_login_wrong_password(live_server, db, page: Page):
    user = UserFactory.create()
    page.goto(live_server.url + "/accounts/login/")
    page.get_by_label("Email address").fill(user.email)
    page.get_by_label("Password").fill("wrongpassword")
    page.get_by_role("button", name="Log in").click()

    # Expect to see an error message.
    error_message = page.get_by_text(
        "Please enter a correct email address and password. Note that both fields may be case-sensitive."
    )
    expect(error_message).to_be_visible()
