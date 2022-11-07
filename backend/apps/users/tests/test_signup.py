from apps.users.factories import UserFactory
from playwright.sync_api import Page, expect


def test_signup_success(live_server, db, page: Page, faker):
    name = faker.name()
    email = faker.email()
    password = faker.password(length=10)

    page.goto(live_server.url + "/signup/")
    page.get_by_label("Full name").fill(name)
    page.get_by_label("Email address").fill(email)

    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_label("Password confirmation").fill(password)
    page.get_by_role("button", name="Sign up").click()

    # Expect to be redirected to the home page.
    expect(page).to_have_url(live_server.url + "/")
    expect(page).to_have_title("WebsiteX")

    # Expect to see a success message.
    success_message = page.get_by_text("Your account has been created.")
    expect(success_message).to_be_visible()

    # Expect to see the user's name in the navbar.
    navbar = page.get_by_role("navigation")
    expect(navbar).to_contain_text(name)


def test_signup_passwords_dont_match(live_server, db, page: Page, faker):
    page.goto(live_server.url + "/signup/")
    page.get_by_label("Full name").fill(faker.name())
    page.get_by_label("Email address").fill(faker.email())

    password = faker.password(length=10)
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_label("Password confirmation").fill("notthesamepassword")
    page.get_by_role("button", name="Sign up").click()

    error_message = page.get_by_text("The two password fields didn’t match.")
    expect(error_message).to_be_visible()


def test_signup_email_already_registered(live_server, db, page: Page, faker):
    user = UserFactory.create()
    page.goto(live_server.url + "/signup/")
    page.get_by_label("Full name").fill(faker.name())
    page.get_by_label("Email address").fill(user.email)

    password = faker.password(length=10)
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_label("Password confirmation").fill(password)
    page.get_by_role("button", name="Sign up").click()

    error_message = page.get_by_text("User with this Email address already exists.")
    expect(error_message).to_be_visible()


def test_signup_password_too_short(live_server, db, page: Page, faker):
    page.goto(live_server.url + "/signup/")
    page.get_by_label("Full name").fill(faker.name())
    page.get_by_label("Email address").fill(faker.email())

    password = faker.password(length=6)
    page.get_by_label("Password", exact=True).fill(password)
    page.get_by_label("Password confirmation").fill(password)
    page.get_by_role("button", name="Sign up").click()

    error_message = page.get_by_text(
        "This password is too short. It must contain at least 8 characters."
    )
    expect(error_message).to_be_visible()
