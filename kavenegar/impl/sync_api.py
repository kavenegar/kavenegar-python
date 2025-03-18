import requests
from typing import Optional, Any, Dict

try:
    import json
except ImportError:
    import simplejson as json  # type: ignore

from ..exceptions import APIException, HTTPException
from .base import KavenegarAPIBase


class KavenegarAPI(KavenegarAPIBase):
    """
    ### Sync version of kavenegar api

    https://kavenegar.com/rest.html
    """

    def __init__(
        self, apikey: str, timeout: Optional[int] = None, proxies: Optional[dict] = None
    ):
        super().__init__(apikey, timeout)
        self._session = requests.Session()
        if proxies:
            self._session.proxies = proxies

    def _request(
        self, action: str, method: str, params: Optional[Dict[str, Any]] = None
    ):
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = self._pars_params_to_json(params)
        url = "https://{}/{}/{}/{}/{}.json".format(
            self.host, self.version, self.apikey, action, method
        )
        try:
            content = self._session.post(
                url, headers=self.headers, auth=None, data=params, timeout=self.timeout
            ).content
            try:
                response = json.loads(content.decode("utf-8"))
                if response["return"]["status"] == 200:
                    return response["entries"]
                else:
                    raise APIException(
                        "APIException[{}] {}".format(
                            response["return"]["status"], response["return"]["message"]
                        )
                    )
            except ValueError as e:
                raise HTTPException(e)
        except requests.exceptions.RequestException as e:
            message = str(e).replace(self.apikey, self.apikey_mask)
            raise HTTPException(message) from None

    def sms_send(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "send", params)

    def sms_sendarray(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "sendarray", params)

    def sms_status(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "status", params)

    def sms_statuslocalmessageid(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "statuslocalmessageid", params)

    def sms_select(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "select", params)

    def sms_selectoutbox(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "selectoutbox", params)

    def sms_latestoutbox(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "latestoutbox", params)

    def sms_countoutbox(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "countoutbox", params)

    def sms_cancel(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "cancel", params)

    def sms_receive(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "receive", params)

    def sms_countinbox(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "countinbox", params)

    def sms_countpostalcode(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "countpostalcode", params)

    def sms_sendbypostalcode(self, params: Optional[Dict[str, Any]] = None):
        return self._request("sms", "sendbypostalcode", params)

    def verify_lookup(self, params: Optional[Dict[str, Any]] = None):
        return self._request("verify", "lookup", params)

    def call_maketts(self, params: Optional[Dict[str, Any]] = None):
        return self._request("call", "maketts", params)

    def call_status(self, params: Optional[Dict[str, Any]] = None):
        return self._request("call", "status", params)

    def account_info(self):
        return self._request("account", "info")

    def account_config(self, params: Optional[Dict[str, Any]] = None):
        return self._request("account", "config", params)
