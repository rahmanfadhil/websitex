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
