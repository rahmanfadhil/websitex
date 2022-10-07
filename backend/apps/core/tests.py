import json
from django.test import Client


def test_js_reverse_view(client: Client):
    response = client.post(
        "/js-reverse/",
        data=json.dumps({"name": "pages:home"}),
        content_type="application/json",
    )
    assert response.status_code == 200
    assert response.content == b"/"


def test_js_reverse_view_invalid_view_name_error(client: Client):
    response = client.post(
        "/js-reverse/",
        data=json.dumps({"name": "invalid_view_name"}),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert response.content == b"No reverse match!"
