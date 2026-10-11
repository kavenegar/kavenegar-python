import pytest
from unittest.mock import patch, MagicMock
from kavenegar import KavenegarAPI, APIException, HTTPException


@pytest.fixture
def api():
    return KavenegarAPI(apikey="1234567890abcdef")


# Helper to mock responses
def mock_response(status=200, entries=None):
    entries = entries or [{"id": 1}]
    response = MagicMock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "return": {"status": status, "message": "OK" if status == 200 else "Error"},
        "entries": entries
    }
    return response


# ------------------------
# Generic test template for all API methods
# ------------------------
@patch("kavenegar.requests.Session.post")
@pytest.mark.parametrize("method_name,params", [
    ("sms_send", {"receptor": "09120000000", "message": "Test"}),
    ("sms_sendarray", {"messages": [{"receptor": "09120000000", "message": "Test"}]}),
    ("sms_status", {"messageid": 12345}),
    ("sms_statuslocalmessageid", {"localid": 1}),
    ("sms_select", {"messageid": 12345}),
    ("sms_selectoutbox", {"page": 1, "row": 10}),
    ("sms_latestoutbox", {"count": 5}),
    ("sms_countoutbox", None),
    ("sms_cancel", {"messageid": 12345}),
    ("sms_receive", None),
    ("sms_countinbox", None),
    ("sms_countpostalcode", {"postalcode": "12345"}),
    ("sms_sendbypostalcode", {"message": "Hello", "postalcode": "12345"}),
    ("verify_lookup", {"receptor": "09120000000", "token": "1234", "template": "verify"}),
    ("call_maketts", {"receptor": "09120000000", "message": "Hello"}),
    ("call_status", {"messageid": 1}),
    ("account_info", None),  # <-- no params
    ("account_config", {"timezone": "Asia/Tehran"})
])
def test_all_methods_success(mock_post, api, method_name, params):
    mocked = mock_response(status=200)
    mock_post.return_value = mocked

    # Only pass params if not None
    if params is not None:
        result = getattr(api, method_name)(params)
    else:
        result = getattr(api, method_name)()

    assert result == [{"id": 1}]
    mock_post.assert_called_once()


# ------------------------
# Test APIException for all methods
# ------------------------
@patch("kavenegar.requests.Session.post")
@pytest.mark.parametrize("method_name", [
    "sms_send", "sms_sendarray", "sms_status", "sms_statuslocalmessageid",
    "sms_select", "sms_selectoutbox", "sms_latestoutbox", "sms_countoutbox",
    "sms_cancel", "sms_receive", "sms_countinbox", "sms_countpostalcode",
    "sms_sendbypostalcode", "verify_lookup", "call_maketts", "call_status",
    "account_info", "account_config"
])
def test_all_methods_api_exception(mock_post, api, method_name):
    fake_response = MagicMock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {
        "return": {"status": 401, "message": "Invalid API key"},
        "entries": []
    }
    mock_post.return_value = fake_response

    with pytest.raises(APIException):
        if method_name in ("account_info",):
            getattr(api, method_name)()
        else:
            getattr(api, method_name)({})


# ------------------------
# Test HTTPException for network errors
# ------------------------
@patch("kavenegar.requests.Session.post")
@pytest.mark.parametrize("method_name,params", [
    ("sms_send", {"receptor": "09120000000", "message": "Test"}),
    ("sms_sendarray", {"messages": [{"receptor": "09120000000", "message": "Test"}]}),
    ("sms_status", {"messageid": 12345}),
    ("sms_statuslocalmessageid", {"localid": 1}),
    ("sms_select", {"messageid": 12345}),
    ("sms_selectoutbox", {"page": 1, "row": 10}),
    ("sms_latestoutbox", {"count": 5}),
    ("sms_countoutbox", None),
    ("sms_cancel", {"messageid": 12345}),
    ("sms_receive", None),
    ("sms_countinbox", None),
    ("sms_countpostalcode", {"postalcode": "12345"}),
    ("sms_sendbypostalcode", {"message": "Hello", "postalcode": "12345"}),
    ("verify_lookup", {"receptor": "09120000000", "token": "1234", "template": "verify"}),
    ("call_maketts", {"receptor": "09120000000", "message": "Hello"}),
    ("call_status", {"messageid": 1}),
    ("account_info", None),  # <-- no params
    ("account_config", {"timezone": "Asia/Tehran"})
])
def test_all_methods_http_exception(mock_post, api, method_name, params):
    mock_post.side_effect = Exception("Network error")

    # Only pass params if not None
    if params is not None:
        with pytest.raises(HTTPException):
            getattr(api, method_name)(params)
    else:
        with pytest.raises(HTTPException):
            getattr(api, method_name)()
