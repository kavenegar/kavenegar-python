import requests
import json

from exceptions import HTTPException, APIException


class KavenegarAPI:
    def __init__(self, apikey: str, timeout: int = 10):
        """
        Default time out is 10 second.
        Host: api.kavenegar.com
        :param apikey:
        :param timeout:
        """
        self._version = 'v1'
        self._host = 'api.kavenegar.com'
        self._apikey = apikey
        self._timeout = timeout
        self._headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'charset': 'utf-8'
        }

    def __repr__(self):
        return f"kavenegar.KavenegarAPI({self._apikey})"

    def __str__(self):
        return f"kavenegar.KavenegarAPI({self._apikey})"

    def _request(self, action, method, params=None):

        if not params:
            params = dict()

        url = f"https://{self._host}/{self._version}/{self._apikey}/{action}/{method}.json"

        try:
            content = requests.post(url, headers=self._headers, auth=None, data=params, timeout=self._timeout).content
            try:
                response = json.loads(content.decode("utf-8"))
                if response['return']['status'] == 200:
                    response = response['entries']
                else:
                    raise APIException(
                        (u'APIException[%s] %s' % (response['return']['status'], response['return']['message'])))
            except ValueError as e:
                raise HTTPException(e)
            return response
        except requests.exceptions.RequestException as e:
            raise HTTPException(e)

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
