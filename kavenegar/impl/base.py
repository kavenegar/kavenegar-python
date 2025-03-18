from typing import Optional, Any

try:
    import json
except ImportError:
    import simplejson as json  # type: ignore

from ..defaults import DEFAULT_TIMEOUT


class KavenegarAPIBase(object):
    """
    https://kavenegar.com/rest.html
    """

    version = "v1"
    host = "api.kavenegar.com"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
        "charset": "utf-8",
    }

    def __init__(self, apikey: str, timeout: Optional[int] = None):
        """
        :param str apikey: Kavengera API Key
        :param int timeout: request timeout, default is 10
        :param dict proxies: Dictionary mapping protocol to the URL of the proxy:
            {
                'http': 'http://192.168.1.10:3128',
                'https': 'http://192.168.1.10:3129',
            }
        """
        self.apikey = apikey
        self.apikey_mask = f"{apikey[:2]}********{apikey[-2:]}"
        self.timeout = timeout or DEFAULT_TIMEOUT

    def __repr__(self):
        return "kavenegar.KavenegarAPI({!r})".format(self.apikey_mask)

    def __str__(self):
        return "kavenegar.KavenegarAPI({!s})".format(self.apikey_mask)

    def _pars_params_to_json(self, params: dict[str, Any]):
        """
        Kavenegar bug, the api server expects the parameters in a JSON-like array format,
        but the requests library form-encode each key-value pair

        Params (dict):
        { sender: ["30002626", "30002627", "30002727", ], }

        request behavior:
        sender=30002626&sender=30002627&sender=30002727

        Server expectation:
        sender=["30002626","30002627","30002727"]
        """
        # Convert lists to JSON-like strings
        formatted_params = {}
        for key, value in params.items():
            if isinstance(value, (dict, list, tuple)):
                formatted_params[key] = json.dumps(value)
            else:
                formatted_params[key] = value
        return formatted_params
