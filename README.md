# kavenegar-python

[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Updated for Modern Python** - This is an actively maintained fork of the Kavenegar Python SDK with support for Python 3.7+ and modern code practices.

# <a href="http://kavenegar.com/rest.html">Kavenegar RESTful API Document</a>
If you need future information about API documentation, please visit the <a href="http://kavenegar.com/rest.html">RESTful API Document</a>

## What's New in This Fork

This updated version includes:
- ✅ **Python 3.7 - 3.12 Support** - Fully compatible with latest Python versions
- ✅ **Modern Python Syntax** - f-strings, class definition updates
- ✅ **Improved Error Handling** - Better exception chaining and JSON error handling
- ✅ **Code Quality Improvements** - Better docstrings, fixed type hints
- ✅ **Updated Tests** - Modern testing patterns with pytest
- ✅ **Clean Code** - Removed legacy Python 2 compatibility code

## Installation

You can install this updated SDK from PyPI:

```bash
pip install kavenegar
```

Or install the latest version from this repository:

```bash
pip install git+https://github.com/hypy13/kavenegar-python.git
```

You can also download the Python SDK <a href="https://github.com/hypy13/kavenegar-python/blob/master/kavenegar.py">directly from here</a>

**Requirements:**
- Python 3.7 or higher
- Create a free account on <a href="https://panel.kavenegar.com/Client/Membership/Register">Kavenegar</a>
- Get your API-KEY from <a href="http://panel.kavenegar.com/Client/setting/index">My Account</a> section

## Usage

Well, there is an example to send SMS using Python below. The `timeout` parameter is optional in `KavenegarAPI` constructor with a default value of 10 seconds.

### Send SMS
```python
from kavenegar import KavenegarAPI, APIException, HTTPException

try:
    api = KavenegarAPI('Your APIKey', timeout=20)
    params = {
        'sender': '',  # optional
        'receptor': '',  # multiple mobile numbers, split by comma
        'message': '',
    } 
    response = api.sms_send(params)
    print(response)
except APIException as e: 
    print(f"API Exception: {e}")
except HTTPException as e: 
    print(f"HTTP Exception: {e}")
```

### OTP (One-Time Password)
```python
from kavenegar import KavenegarAPI, APIException, HTTPException

try:
    api = KavenegarAPI('Your APIKey', timeout=20)
    params = {
        'receptor': '',
        'template': '',
        'token': '',
        'type': 'sms',  # 'sms' or 'call'
    }   
    response = api.verify_lookup(params)
    print(response)
except APIException as e: 
    print(f"API Exception: {e}")
except HTTPException as e: 
    print(f"HTTP Exception: {e}")
```

### Send Bulk SMS
```python
from kavenegar import KavenegarAPI, APIException, HTTPException

try:
    api = KavenegarAPI('Your APIKey', timeout=20)
    params = {
        'sender': '["",""]',  # array of strings as JSON 
        'receptor': '["",""]',  # array of strings as JSON 
        'message': '["",""]',  # array of strings as JSON 
    } 
    response = api.sms_sendarray(params)
    print(response)
except APIException as e: 
    print(f"API Exception: {e}")
except HTTPException as e: 
    print(f"HTTP Exception: {e}")
```

## Python Version Compatibility

| Python Version | Status |
|---|---|
| 3.7 | ✅ Supported |
| 3.8 | ✅ Supported |
| 3.9 | ✅ Supported |
| 3.10 | ✅ Supported |
| 3.11 | ✅ Supported |
| 3.12 | ✅ Supported |
| 2.7 | ❌ Not supported |

## Troubleshooting

**Issue:** `ModuleNotFoundError: No module named 'kavenegar'`
- **Solution:** Make sure to install the package using `pip install kavenegar`

**Issue:** `APIException` errors
- **Solution:** Verify your API key is correct and has the necessary permissions

**Issue:** `HTTPException` errors
- **Solution:** Check your internet connection and Kavenegar API status

## Contribution

Bug fixes, documentation, and enhancements are welcome! 

To contribute:
1. Fork this repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

For issues and feature requests: <a href="mailto:support@kavenegar.com?Subject=SDK" target="_top">support@kavenegar.com</a>

---

<div dir='rtl'>

## راهنما (Persian Guide)

### معرفی سرویس کاوه نگار

کاوه ��گار یک وب سرویس ارسال و دریافت پیامک و تماس صوتی است که به راحتی میتوانید از آن استفاده نمایید.

### ساخت حساب کاربری

اگر در وب سرویس کاوه نگار عضو نیستید میتوانید از [لینک عضویت](http://panel.kavenegar.com/client/membership/register) ثبت نام و اکانت بسازید.

### مستندات

برای مشاهده اطلاعات کامل مستندات [وب سرویس پیامک](http://kavenegar.com/وب-سرویس-پیامک.html) به صفحه [مستندات وب سرویس](http://kavenegar.com/rest.html) مراجعه نمایید.

### راهنمای فارسی

در صورتی که مایل هستید راهنمای فارسی کیت توسعه کاوه نگار را مطالعه کنید به صفحه [کد ارسال پیامک](http://kavenegar.com/sdk-index.html) مراجعه نمایید.

### اطالاعات بیشتر
برای مطالعه بیشتر به صفحه معرفی [وب سرویس اس ام اس](http://kavenegar.com) کاوه نگار مراجعه نمایید.

اگر در استفاده از کیت های سرویس کاوه نگار مشکلی یا پیشنهادی داشتید ما را با یک Pull Request یا ارسال ایمیل به support@kavenegar.com اطلاع دهید.

</div>

---

![Kavenegar](http://kavenegar.com/public/images/logo.png)

[http://kavenegar.com](http://kavenegar.com)
