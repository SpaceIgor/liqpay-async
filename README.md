[![Python 3.6+](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)

[![SDK-Python3](https://www.liqpay.ua/logo_liqpay_main.svg)](https://www.liqpay.ua/documentation/api/home)

* Web: https://www.liqpay.ua/
* Source: https://github.com/SpaceIgor/liqpay-async
* Documentation: https://www.liqpay.ua/documentation/en/
* Keywords: liqpay, privat24, privatbank, python, internet acquiring, P2P payments, two-step payments


What python version is supported?
============
- Python 3.4+

Get Started
============
1. Sign up in https://www.liqpay.ua/en/authorization.
2. Create a company.
3. In company settings, on API tab, get **Public key** and **Private key**: https://www.liqpay.ua/doc
4. Done.

Installation
============
From pip
```pip install liqpay-async```

Working with LiqPay Callback locally
============
If you need debugging API Callback on local environment use https://localtunnel.github.io/www/

How it uses?
============

Example 1: Pin token card to user
-------

**Backend**
Get url on SDK 

Request url: https://www.liqpay.ua/api/3/checkout

```python
from liqpay_async import LiqPay

liqpay_manager = LiqPay(public_key, private_key)
response = await liqpay_manager.post( 
        return_url=True,
        data={
            "action": "hold",
            "version": "3",
            "amount": "1",
            "currency": "UAH",  # or any currency
            "description": "Pin card",
            "language": "uk|en"     # liqpay have only ("uk", "en)
            "order_id": f"{id_user from token} {str(uuid.uuid4())}",    # id_user from token need for pin card to user
            "server_url": f"{YOUR_HOST}{URL}",  # for callback response
            "recurringbytoken": "1",    # for get token in response callback
        },
    )
    
    # check on bad response
    if response["status"] in (0, 1):
        # when response status 0 or 1 from response dict u can get key 'err_code' - https://www.liqpay.ua/doc/api/errors
        raise
    
# OK response - {"url: url, status: STATUS_MAPPING}
# return url on SDK

# When u sent card credentials in checkout SDK LiqPay. U get response on the url(server_url) from request dict
#Example:

from fastapi import Request, Body

LIQPAY_DOMAIN = "liq_pay domain"

async def pin_card(
        request: Request,
        liq_pay: YourModel = Body(...),
):
    origin = request.headers.get("origin")
    if not origin or origin != LIQPAY_DOMAIN:   # for security
        raise 
    
    data = liq_pay.order_id.split()

    await liqpay_manager.post(
                data={
                    "action": "refund",     # refund money
                    "version": "3",
                    "order_id": liq_pay.order_id,
                }
            )

    # and save data from callback

    # data[0] - its id user from order_id
    # card_token, sender_card_mask2, sender_card_type

```

Example 2: For other operation by token card
-------

**Backend**

Request url: https://www.liqpay.ua/api/request

```python
from liqpay_async import LiqPay

liqpay_manager = LiqPay(public_key, private_key)

# https://www.liqpay.ua/doc/api/internet_acquiring/checkout?tab=1
response = await liqpay_manager.post( 
        data={
            "action": "your action",
            "version": "3",
            "amount": "1",
            "currency": "UAH",  # or any currency
            "description": "Your desc",
            "language": "uk|en"     # liqpay have only ("uk", "en)
            "order_id": "str(uuid.uuid4())",
            "card_token": your_card_token
        },
    )
    
# OK response - {status: STATUS_MAPPING and others)


```

Example 3: Errors
-------

**Backend**

```python

# if response aiothhp error -> response {"status": 0}


```