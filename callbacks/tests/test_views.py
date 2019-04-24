import uuid
import pytest
from unittest.mock import MagicMock

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
def test_callback_view_always_return_200(method, monkeypatch):
    monkeypatch.setattr("callbacks.views.async_to_sync", lambda x: lambda x, y: None)
    callback = uuid.uuid4()
    c = Client()
    response = getattr(c, method)(reverse("callback-submit", kwargs={"uuid": callback}))
    assert response.status_code == 200


def test_callback_view_submits_request_info_to_channel_layer(monkeypatch):
    mock = MagicMock()
    request_data = {"body": {"some": "data"}, "headers": {"header": "one"}}
    monkeypatch.setattr("callbacks.views.async_to_sync", lambda x: mock)
    monkeypatch.setattr(
        "callbacks.views.CallbackView._request_data", lambda x, y: request_data
    )
    callback = str(uuid.uuid4())
    response = Client().post(
        reverse("callback-submit", kwargs={"uuid": callback}),
        data={"some": "data"},
        headers={"header": "one"},
    )
    assert response.status_code == 200
    mock.assert_called_with(callback, {"type": "new_request", "data": request_data})


def test_callback_view_filters_excluded_headers(settings, monkeypatch):
    settings.EXCLUDED_HEADERS = ["Excluded"]
    mock = MagicMock()
    monkeypatch.setattr("callbacks.views.async_to_sync", lambda x: mock)
    callback = str(uuid.uuid4())
    response = Client().post(
        reverse("callback-submit", kwargs={"uuid": callback}),
        HTTP_not_excluded="one",
        HTTP_excluded="two",
    )
    cb, all_data = mock.call_args[0]
    assert response.status_code == 200
    assert callback == cb
    data = all_data["data"]
    assert "headers" in data
    assert "Excluded" not in data["headers"].keys()
    assert "Not-Excluded" in data["headers"].keys()


@pytest.mark.parametrize("status", [200, 201, 400, 401, 403, 404, 500])
def test_callback_view_non_default_response(status, monkeypatch):
    monkeypatch.setattr("callbacks.views.async_to_sync", lambda x: lambda x, y: None)
    callback = uuid.uuid4()
    res = Client().get(
        reverse("callback-submit-response", kwargs={"uuid": callback, "status": status})
    )
    assert res.status_code == status
