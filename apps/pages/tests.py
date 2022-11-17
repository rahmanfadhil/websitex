import re

from playwright.sync_api import Page, expect


def test_home_page_respond_successfully(db, client):
    response = client.get("/")
    assert response.status_code == 200


def test_home_page_get_started_button_goes_to_login_page(live_server, page: Page):
    page.goto(live_server.url)

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("WebsiteX"))

    # create a locator
    get_started = page.locator("text=Get Started")

    # Expect an attribute "to be strictly equal" to the value.
    expect(get_started).to_have_attribute("href", "/accounts/login/")

    # Click the get started link.
    get_started.click()

    # Expect to be redirected to the login page.
    expect(page).to_have_url(live_server.url + "/accounts/login/")
    expect(page).to_have_title("Login - WebsiteX")


def test_home_page_login_button_goes_to_login_page(live_server, page: Page):
    page.goto(live_server.url)

    # Click the button.
    page.locator("text=Log in").click()

    # Expect to be redirected to the login page.
    expect(page).to_have_url(live_server.url + "/accounts/login/")
    expect(page).to_have_title("Login - WebsiteX")


def test_home_page_signup_button_goes_to_signup_page(live_server, page: Page):
    page.goto(live_server.url)

    # Click the button.
    page.locator("text=Sign up").click()

    # Expect to be redirected to the signup page.
    expect(page).to_have_url(live_server.url + "/signup/")
    expect(page).to_have_title("Sign up - WebsiteX")
