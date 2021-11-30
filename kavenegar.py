import requests

try:
    import json
except ImportError:
    import simplejson as json

# Default requests timeout in seconds.
DEFAULT_TIMEOUT = 10


class APIException(Exception):
    pass

    def __str__(self):
        return f'APIException[{self.status_code}] {self.message}'


class KavenegarAPI(object):
    def __init__(self, apikey, timeout=None):
        self.version = 'v1'
        self.host = 'api.kavenegar.com'
        self.apikey = apikey
        self.timeout = timeout or DEFAULT_TIMEOUT
        self.headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded',
            'charset': 'utf-8'
        }

    def __repr__(self):
        return f'kavenegar.KavenegarAPI({self.apikey})'

    def __str__(self):
        return f'kavenegar.KavenegarAPI({self.apikey})'

    def _request(self, action, method, params=None):
        if params is None:
            params = {}

        url = f'https://{self.host}/{self.version}/{self.apikey}/{action}/{method}.json'
        try:
            content = requests.post(url, headers=self.headers, auth=None, data=params, timeout=self.timeout).content
            try:
                response = json.loads(content.decode('utf-8'))
                if response['return']['status'] == 200:
                    response = response['entries']
                else:
                    raise APIException('APIException[{}] {}'.format(response['return']['status'],response['return']['message']))
            except ValueError as e:
                raise HTTPException(e)
            return response
        except requests.exceptions.RequestException as e:
            raise HTTPException(e)

    def sms_send(self, params=None):
        return self._request('sms', 'send', params)

    def sms_send_array(self, params=None):
        return self._request('sms', 'sendarray', params)

    def sms_status(self, params=None):
        return self._request('sms', 'status', params)

    def sms_status_local_message_id(self, params=None):
        return self._request('sms', 'statuslocalmessageid', params)

    def sms_select(self, params=None):
        return self._request('sms', 'select', params)

    def sms_select_outbox(self, params=None):
        return self._request('sms', 'selectoutbox', params)

    def sms_latest_outbox(self, params=None):
        return self._request('sms', 'latestoutbox', params)

    def sms_count_outbox(self, params=None):
        return self._request('sms', 'countoutbox', params)

    def sms_cancel(self, params=None):
        return self._request('sms', 'cancel', params)

    def sms_receive(self, params=None):
        return self._request('sms', 'receive', params)

    def sms_count_inbox(self, params=None):
        return self._request('sms', 'countinbox', params)

    def sms_count_postal_code(self, params=None):
        return self._request('sms', 'countpostalcode', params)

    def sms_send_by_postal_code(self, params=None):
        return self._request('sms', 'sendbypostalcode', params)

    def verify_lookup(self, params=None):
        return self._request('verify', 'lookup', params)

    def call_make_tts(self, params=None):
        return self._request('call', 'maketts', params)

    def call_status(self, params=None):
        return self._request('call', 'status', params)

    def account_info(self):
        return self._request('account', 'info')

    def account_config(self, params=None):
        return self._request('account', 'config', params)
