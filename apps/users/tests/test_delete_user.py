from apps.users.models import User
from playwright.sync_api import Page, expect


def test_delete_user(live_server, e2e_user, page: Page):
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
    expect(page.get_by_role("heading", name="Delete account")).to_be_visible()
    page.get_by_role("button", name="Delete account").click()
    page.get_by_role("button", name="Yes, delete my account").click()

    # Expect to be redirected to the home page.
    expect(page).to_have_url(live_server.url + "/")
    expect(page.get_by_role("navigation")).not_to_contain_text(e2e_user.full_name)

    # Expect the user to be deleted.
    assert not User.objects.filter(pk=e2e_user.pk).exists()
