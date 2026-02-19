import requests, base64, datetime, json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def generate_timestamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def generate_password():
    timestamp = generate_timestamp()
    data_to_encode = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    encoded = base64.b64encode(data_to_encode.encode("utf-8")).decode("utf-8")
    return encoded


def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=(settings.CONSUMER_KEY, settings.CONSUMER_SECRET))
    response.raise_for_status()  
    return response.json().get("access_token")


def lipa_na_mpesa(phone, amount):
    try:
        access_token = get_access_token()
        api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        timestamp = generate_timestamp()
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,   
            "Password": generate_password(),
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone,  
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": phone,
            "CallBackURL": settings.MPESA_CALLBACK_URL,  
            "AccountReference": "MadolaRestaurant",
            "TransactionDesc": "Food Order Payment",
        }

        response = requests.post(api_url, json=payload, headers=headers)
        print("🔹 Raw Response:", response.text)  

        return response.json()  
    except Exception as e:
        print(" Error in lipa_na_mpesa:", e)
        return {"errorMessage": str(e)}


@csrf_exempt
def mpesa_callback(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        print("📩 M-Pesa Callback:", data)

        body = data.get("Body", {}).get("stkCallback", {})
        result_code = body.get("ResultCode")

        if result_code == 0: 
            meta = body.get("CallbackMetadata", {}).get("Item", [])
            phone = next((x["Value"] for x in meta if x["Name"] == "PhoneNumber"), None)
            amount = next((x["Value"] for x in meta if x["Name"] == "Amount"), None)
            receipt = next((x["Value"] for x in meta if x["Name"] == "MpesaReceiptNumber"), None)

            # 🔹 Save to DB
            from restaurant.models import Payment
            try:
                payment = Payment.objects.filter(status="pending", phone=phone).last()
                if payment:
                    payment.status = "success"
                    payment.mpesa_code = receipt
                    payment.amount = amount
                    payment.save()

                    if payment.order:
                        payment.order.status = "paid"
                        payment.order.save()

                print(f" Payment updated: {receipt} | {amount} | {phone}")
            except Exception as e:
                print(" Error updating payment:", e)

        else:  
            print(" Payment Failed:", body)

        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

    except Exception as e:
        print(" Callback Error:", e)
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Failed"})
