<a href="http://kavenegar.com">
    <img width="300px" src="http://kavenegar.com/images/logo.svg" />
</a>

# Kavenegar Python Client

[![PyPI version](https://badge.fury.io/py/kavenegar.svg)](https://badge.fury.io/py/kavenegar)

For more information about Kavenegar RESTful API, you can visit <a href="http://kavenegar.com/rest.html" target="_blank">Kavenegar RESTful API documnets</a>.

## Installation

<p>Use the following command to install Kavenegar python client:</p>

```
pip install kavenegar
```

After the installation completed, create your Kavenegar account from <a href="https://panel.kavenegar.com/Client/Membership/Register">here</a>. Then you can access to your `API-KEY` from <a href="http://panel.kavenegar.com/Client/setting/account">your account settings section</a>.

## Usage

Well, here you can find some examples on how to use `kavenegar` for sending sms, one-time password (OTP) and group sms. `timeout` parameter is optional in `KavenegarAPI` constructor and you can specify this as much as you want (default value is 10 seconds).

### Send SMS

```python
from kavenegar import *

try:
    api = KavenegarAPI('Your APIKey', timeout=20)
    params = {
        'sender': '10006001001010', # optional
        'receptor': '09123456789', # multiple mobile number, splited by comma.
        'message': 'Your message here!'
    }
    response = api.sms_send(params)
    print(response)
except APIException as e:
    print(e)
except HTTPException as e:
    print(e)
```

### Send OTP

```python
from kavenegar import *

try:
    api = KavenegarAPI('Your APIKey', timeout=20)
    params = {
        'receptor': '09123456789',
        'template': '',
        'token': 'The token here!',
        'type': 'sms' # You can use sms or call
    }
    response = api.verify_lookup(params)
    print(response)
except APIException as e:
    print(e)
except HTTPException as e:
    print(e)
```

### Send Bulk SMS

```python
from kavenegar import *

try:
    api = KavenegarAPI('Your APIKey', timeout=20)
    params = {
        'sender': '["10006001001010", "10001000033300"]',
        'receptor': '["09123456789", "09123456788"]',
        'message': '["Your message here!", "Another message here!"]'
    }
    response = api.sms_sendarray(params)
    print(response)
except APIException as e:
    print(e)
except HTTPException as e:
    print(e)
```

# Kavenegar Guide

## Kavenegar Introduction

Kavenegar is service that is easy to use for send and receive sms and voice calls.

## Create Account

If you didn't join us already, use <a href="http://panel.kavenegar.com/client/membership/register">registration page</a>.

## Documents

For more information about <a href="http://kavenegar.com/وب-سرویس-پیامک.htm">Kavenegar sms service</a>, follow <a href="http://kavenegar.com/rest.html">RESTful API documents</a>.

## Persian Guide

You can find persian documents of different Kavenegar clients, <a href="http://kavenegar.com/sdk.html">here</a>.

# Contribution

Feel free to report any bug or problem by creating issue or sending email to our support team, or enhance docs or code and so on by creating PR (You can use this <a href="http://gun.io/blog/how-to-github-fork-branch-and-pull-request/">tutorial</a> to learn how to create fork from a project ,then create PR to main project).
For more information, visit <a href="http://kavenegar.com">our website</a>.
Contact us <a href="mailto:support@kavenegar.com?Subject=SDK" target="_top">support@kavenegar.com</a>.

</div>
