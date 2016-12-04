# kavenegar-php

Installation
-----
Basic setup
-----
Configuration
-----
Usage
-----
```python
#!/usr/bin/env python
from kavenegar import *
try:
    import json
except ImportError:
    import simplejson as json
	
try:
	api = KavenegarAPI('{Your APIKey}')
	params = {
		'sender': '10004346',
		'receptor': '09123456789,09367891011',
		'message': 'خدمات پیام کوتاه کاوه نگار'
	}   
	response = api.sms_send(params)
	print str(response)
except APIException,e: 
	print str(e)
except HTTPException,e: 
	print str(e)

'''
sample output
{
    "return":
    {
        "status":200,
        "message":"تایید شد"
    },
    "entries": 
    [
        {
            "messageid":8792343,
            "message":"خدمات پیام کوتاه کاوه نگار",
            "status":1,
            "statustext":"در صف ارسال",
            "sender":"10004346",
            "receptor":"09123456789",
            "date":1356619709,
            "cost":120
        },
        {
            "messageid":8792344,
            "message":"خدمات پیام کوتاه کاوه نگار",
            "status":1,
            "statustext":"در صف ارسال",
            "sender":"10004346",
            "receptor":"09367891011",
            "date":1356619709,
            "cost":120
        }
    ]
}
'''
```
