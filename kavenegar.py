import requests
import json

# Default requests timeout in seconds.
DEFAULT_TIMEOUT = 10


class APIException(Exception):
    pass


class HTTPException(Exception):
    pass


class KavenegarAPI:
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

    def __init__(self, apikey, timeout=None, proxies=None, pool_connections=10, pool_maxsize=20, pool_block=True):
        """
        :param str apikey: Kavenegar API Key
        :param int timeout: request timeout, default is 10
        :param dict proxies: Dictionary mapping protocol to the URL of the proxy:
            {
                'http': 'http://192.168.1.10:3128',
                'https': 'http://192.168.1.10:3129',
            }
        :param int pool_connections: number of connection pools (urllib3)
        :param int pool_maxsize: max connections per pool
        """
        self.apikey = apikey
        self.apikey_mask = f"{apikey[:2]}********{apikey[-2:]}"
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.proxies = proxies

        self.session = requests.Session()

        adapter = requests.adapters.HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            pool_block=pool_block
        )

        self.session.mount('https://', adapter)
        self.session.headers.update(self.headers)

    def __repr__(self):
        return f"kavenegar.KavenegarAPI({self.apikey_mask!r})"

    def __str__(self):
        return f"kavenegar.KavenegarAPI({self.apikey_mask!s})"

    def close(self):
        """Close all pooled connections"""
        self.session.close()

    def _pars_params_to_json(self, params):
        """Convert lists and dicts to JSON-like strings"""
        formatted_params = {}
        for key, value in params.items():
            if isinstance(value, (dict, list, tuple)):
                formatted_params[key] = json.dumps(value)
            else:
                formatted_params[key] = value
        return formatted_params

    def _request(self, action, method, params=None):
        if params is None:
            params = {}
        if isinstance(params, dict):
            params = self._pars_params_to_json(params)
        url = f"https://{self.host}/{self.version}/{self.apikey}/{action}/{method}.json"
        try:
            response = self.session.post(
                url,
                headers=self.headers,
                auth=None,
                data=params,
                timeout=self.timeout,
                proxies=self.proxies,
            )
            response.raise_for_status()  # Raises HTTPError for 4xx/5xx

            try:
                json_response = response.json()
                if json_response['return']['status'] == 200:
                    return json_response['entries']
                else:
                    raise APIException(
                        f"APIException[{json_response['return']['status']}] {json_response['return']['message']}"
                    )
            except json.JSONDecodeError as e:
                raise HTTPException(f"Invalid JSON response: {e}") from e
        except requests.exceptions.RequestException as e:
            message = str(e).replace(self.apikey, self.apikey_mask)
            raise HTTPException(message) from e

    def sms_send(self, params=None):
        return self._request('sms', 'send', params)

    def sms_sendarray(self, params=None):
        return self._request('sms', 'sendarray', params)

    def sms_status(self, params=None):
        return self._request('sms', 'status', params)

    def sms_statuslocalmessageid(self, params=None):
        return self._request('sms', 'statuslocalmessageid', params)

    def sms_select(self, params=None):
        return self._request('sms', 'select', params)

    def sms_selectoutbox(self, params=None):
        return self._request('sms', 'selectoutbox', params)

    def sms_latestoutbox(self, params=None):
        return self._request('sms', 'latestoutbox', params)

    def sms_countoutbox(self, params=None):
        return self._request('sms', 'countoutbox', params)

    def sms_cancel(self, params=None):
        return self._request('sms', 'cancel', params)

    def sms_receive(self, params=None):
        return self._request('sms', 'receive', params)

    def sms_countinbox(self, params=None):
        return self._request('sms', 'countinbox', params)

    def sms_countpostalcode(self, params=None):
        return self._request('sms', 'countpostalcode', params)

    def sms_sendbypostalcode(self, params=None):
        return self._request('sms', 'sendbypostalcode', params)

    def verify_lookup(self, params=None):
        return self._request('verify', 'lookup', params)

    def call_maketts(self, params=None):
        return self._request('call', 'maketts', params)

    def call_status(self, params=None):
        return self._request('call', 'status', params)

    def account_info(self):
        return self._request('account', 'info')

    def account_config(self, params=None):
        return self._request('account', 'config', params)
