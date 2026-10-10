import json
from unittest.mock import patch

import pytest
import requests

from kavenegar import APIException, HTTPException, KavenegarAPI


@pytest.fixture
def client():
    api = KavenegarAPI("0123456789abcdef")
    try:
        yield api
    finally:
        api.close()


def response_for(client, status, payload):
    response = requests.Response()
    response.status_code = status
    response.url = "https://api.kavenegar.com/v1/{}/account/info.json".format(client.apikey)
    response.encoding = "utf-8"
    response._content = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return response


@pytest.mark.parametrize("status", [400, 401, 403, 418, 422, 503])
def test_provider_http_errors_raise_api_exception(client, status):
    message = "پارامترهای ورودی معتبر نیستند"
    response = response_for(client, status, {"return": {"status": status, "message": message}, "entries": None})

    with patch.object(client.session, "post", return_value=response):
        with pytest.raises(APIException) as error:
            client.account_info()

    assert str(error.value) == "APIException[{}] {}".format(status, message)


def test_provider_error_in_successful_http_response_raises_api_exception(client):
    response = response_for(client, 200, {"return": {"status": 403, "message": "Invalid API key"}, "entries": None})

    with patch.object(client.session, "post", return_value=response):
        with pytest.raises(APIException, match=r"APIException\[403\] Invalid API key"):
            client.account_info()


def test_successful_response_returns_entries(client):
    entries = [{"remaincredit": 1234}]
    response = response_for(client, 200, {"return": {"status": 200, "message": "OK"}, "entries": entries})

    with patch.object(client.session, "post", return_value=response):
        assert client.account_info() == entries


def test_http_error_with_successful_provider_payload_raises_http_exception(client):
    response = response_for(client, 503, {"return": {"status": 200, "message": "OK"}, "entries": []})

    with patch.object(client.session, "post", return_value=response):
        with pytest.raises(HTTPException, match="503"):
            client.account_info()


@pytest.mark.parametrize("status", [200, 400, 503])
def test_non_json_response_raises_http_exception(client, status):
    response = response_for(client, status, None)
    response._content = b"<html>Service unavailable</html>"

    with patch.object(client.session, "post", return_value=response):
        with pytest.raises(HTTPException) as error:
            client.account_info()

    if status == 200:
        assert "Invalid JSON response" in str(error.value)
    else:
        assert str(status) in str(error.value)
        assert client.apikey not in str(error.value)
        assert client.apikey_mask in str(error.value)


@pytest.mark.parametrize("status", [400, 503])
def test_non_provider_json_http_error_raises_http_exception(client, status):
    response = response_for(client, status, {"error": "Service unavailable"})

    with patch.object(client.session, "post", return_value=response):
        with pytest.raises(HTTPException, match=str(status)):
            client.account_info()


@pytest.mark.parametrize("payload", [{}, {"return": None}, []])
def test_invalid_provider_payload_raises_http_exception(client, payload):
    response = response_for(client, 200, payload)

    with patch.object(client.session, "post", return_value=response):
        with pytest.raises(HTTPException, match="Invalid API response"):
            client.account_info()


@pytest.mark.parametrize("exception_type", [requests.exceptions.ConnectionError, requests.exceptions.Timeout])
def test_transport_errors_raise_http_exception_and_mask_api_key(client, exception_type):
    error_message = "Request failed for https://api.kavenegar.com/v1/{}/account/info.json".format(client.apikey)

    with patch.object(client.session, "post", side_effect=exception_type(error_message)):
        with pytest.raises(HTTPException) as error:
            client.account_info()

    assert str(error.value) == error_message.replace(client.apikey, client.apikey_mask)
