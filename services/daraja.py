import requests
from fastapi import HTTPException
import json
import base64
from datetime import datetime
from core.config import settings
if settings.MPESA_ENV =="production":
    BASE_URL="https://api.safaricom.co.ke"
else:
    BASE_URL="https://sandbox.safaricom.co.ke"
def get_access_token():
    url=f"{BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response=requests.get(url,auth=(settings.MPESA_CONSUMER_KEY,settings.MPESA_CONSUMER_SECRET))
    if response.status_code != 200:
        raise HTTPException(502,detail=f"Daraja auth failed: {response.text}")
    return response.json()["access_token"]
def generate_password():
    timestamp=datetime.now().strftime("%Y%m%d%H%M%S")
    data=(settings.MPESA_SHORTCODE.strip() + settings.MPESA_PASSKEY.strip() + timestamp)
    password=base64.b64encode(data.encode()).decode("utf-8")
    decode=base64.b64decode(password).decode()
    return password, timestamp
def call_daraja_api(phone,amount,reference):
    access_token=get_access_token()
    password,timestamp=generate_password()
    url=f"{BASE_URL}/mpesa/stkpush/v1/processrequest"
    payload={
        "BusinessShortCode":settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp":timestamp,
        "TransactionType": "CustomerBuyGoodsOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": settings.MPESA_TILL,
        "PhoneNumber":phone,
        "CallBackURL":settings.MPESA_CALLBACK_URL,
        "AccountReference":reference,
        "TransactionDesc": "test"
    }
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    print(json.dumps(payload, indent=2))
    response = requests.post(url,json=payload,headers=headers)
    print("STK RESPONSE:",response)
    try:
        data=response.json()
    except ValueError:
        raise HTTPException(502,detail=f"Mpesa API returned invalid response: {response.text}")
    return data
