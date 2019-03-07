import uuid
import pytest

from django.test import Client
from django.urls import reverse


def test_home_view_redirects_random_callback_page():
    response = Client().get(reverse("callback-home"))
    assert response.status_code == 302
    assert reverse("callback-check") in response["Location"]


def test_check_callback_renders_template():
    callback = uuid.uuid4()
    response = Client().get(reverse("callback-check"), cb=str(callback))
    assert response.status_code == 200
    assert "callbacks/check.html" == response.templates[0].name


@pytest.mark.parametrize(
    "method", ["get", "put", "post", "head", "delete", "patch", "options"]
)
def test_callback_view_always_return_200(method):
    callback = uuid.uuid4()
    c = Client()
    response = getattr(c, method)(reverse("callback-submit", kwargs={"uuid": callback}))
    assert response.status_code == 200


def test_callback_view_submits_request_info_to_channel_layer():
    # TODO
    pass
