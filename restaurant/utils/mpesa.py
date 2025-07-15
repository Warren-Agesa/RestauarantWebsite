# utils/mpesa.py
import requests
from requests.auth import HTTPBasicAuth
import datetime
import base64

def lipa_na_mpesa(phone_number, amount):
    consumer_key = 'jWPLwGxfoLBFvKHRkMulzLdyAYQRjGKOEL4bljPIwKH4YPG5'
    consumer_secret = 'fn2rCBJT6VKGWyIAZvbyGkCvfo55fuG47lA7dbPZSroFUPxGkz2UexSuw5y0wvUK'
    shortcode = '174379'  # Default sandbox shortcode
    passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'

    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = shortcode + passkey + timestamp
    password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    # Step 1: Generate access token
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth_response = requests.get(auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = auth_response.json().get('access_token')

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Step 2: Prepare STK Push request
    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": phone_number,
        "PartyB": shortcode,
        "PhoneNumber": phone_number,
        "CallBackURL": "https://yourdomain.com/callback/",
        "AccountReference": "Madola",
        "TransactionDesc": "Payment for food order"
    }

    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        headers=headers,
        json=payload
    )
    return response.json()
