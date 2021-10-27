def test_home_page_render_successfully(client):
    response = client.get("/")
    assert response.status_code == 200
