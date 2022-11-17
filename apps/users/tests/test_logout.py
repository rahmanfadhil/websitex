from playwright.sync_api import Page, expect
from apps.users.models import User


def test_logout_success(live_server, db, page: Page, e2e_user: User):
    page.goto(live_server.url)

    # Expect to see the user's name in the navbar.
    navbar = page.get_by_role("navigation")
    expect(navbar).to_contain_text(e2e_user.full_name)

    # Click the user's name in the navbar.
    navbar.get_by_role("button", name=e2e_user.full_name).click()
    # Click the "Log out" button in the dropdown.
    navbar.get_by_role("button", name="Log out").click()

    # Expect the modal to be visible.
    expect(page.get_by_text("Are you sure you want to log out?")).to_be_visible()
    # Click the "Log out" button in the modal.
    page.get_by_role("button", name="Yes, log out").click()

    # Expect to be redirected to the home page.
    expect(page).to_have_url(live_server.url + "/")
    expect(page.get_by_role("navigation")).not_to_contain_text(e2e_user.full_name)
