from apps.users.models import User
from playwright.sync_api import Page, expect


def test_change_password(live_server, e2e_user: User, page: Page, faker):
    page.goto(live_server.url)

    # Expect to see the user's name in the navbar.
    navbar = page.get_by_role("navigation")
    expect(navbar).to_contain_text(e2e_user.full_name)

    # Click the user's name in the navbar.
    navbar.get_by_role("button", name=e2e_user.full_name).click()
    # Click the "Settings" link in the dropdown.
    navbar.get_by_role("link", name="Settings").click()

    # Expect to be redirected to the user settings page.
    expect(page).to_have_url(live_server.url + "/accounts/update/")
    expect(page.get_by_role("heading", name="Change password")).to_be_visible()
    page.get_by_role("link", name="Change my password").click()

    # Expect to be redirected to the change password page.
    expect(page).to_have_url(live_server.url + "/accounts/password_change/")
    expect(page.get_by_role("heading", name="Change password")).to_be_visible()
    new_password = faker.password(length=12)
    page.get_by_label("Old password").fill("12345")
    page.get_by_label("New password", exact=True).fill(new_password)
    page.get_by_label("New password confirmation").fill(new_password)
    page.get_by_role("button", name="Change my password").click()

    # Expect to be redirected to the change password done page.
    expect(page).to_have_url(live_server.url + "/accounts/password_change/done/")
    expect(page.get_by_role("heading", name="Password changed!")).to_be_visible()
    page.get_by_role("link", name="Back to home").click()

    # Expect to be redirected to the home page.
    expect(page).to_have_url(live_server.url + "/")
    expect(page.get_by_role("navigation")).to_contain_text(e2e_user.full_name)

    # Log out.
    navbar.get_by_role("button", name=e2e_user.full_name).click()
    navbar.get_by_role("button", name="Log out").click()
    page.get_by_role("button", name="Yes, log out").click()

    # Expect to be redirected to the home page.
    expect(page).to_have_url(live_server.url + "/")
    expect(page.get_by_role("navigation")).not_to_contain_text(e2e_user.full_name)

    # Go to the login page.
    page.goto(live_server.url + "/accounts/login/")
    page.get_by_label("Email address").fill(e2e_user.email)
    page.get_by_label("Password").fill(new_password)
    page.get_by_role("button", name="Log in").click()

    # Expect to be redirected to the home page.
    expect(page).to_have_url(live_server.url + "/")
    expect(page.get_by_role("navigation")).to_contain_text(e2e_user.full_name)
