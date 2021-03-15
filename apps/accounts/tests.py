from pytest_django.asserts import assertTemplateUsed


def test_home_page_render_successfully(client):
    response = client.get("/")
    assert response.status_code == 200
    assertTemplateUsed(response, "pages/home.html")


def test_about_page_render_successfully(client):
    response = client.get("/about/")
    assert response.status_code == 200
    assertTemplateUsed(response, "pages/about.html")
