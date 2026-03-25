from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
import base64
import os
from datetime import datetime

router = APIRouter()

# Daraja API credentials
CONSUMER_KEY = "LM6MxKjJXDzqIxYK7ej1A6DWUd8sVJ6XYf22ByFh4R4rgykA"
CONSUMER_SECRET = "MAjliohCqtGGvshySY8RkHZSF88eemW1Wp77PjwxO3ci0m7242fdGGEXv2TQkljk"
PASSKEY = "d4f1dd629fbd7638a5272362f3b42057bf5fed09bca901db242b0ac7e88ee993"
SHORTCODE = "3538431"
CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL", "https://portifolio.azurewebsites.net/mpesa/callback")

DARAJA_BASE = "https://api.safaricom.co.ke"


def get_access_token() -> str:
    credentials = base64.b64encode(f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()).decode()
    response = requests.get(
        f"{DARAJA_BASE}/oauth/v1/generate?grant_type=client_credentials",
        headers={"Authorization": f"Basic {credentials}"},
        timeout=15
    )
    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Failed to get M-Pesa access token")
    return response.json()["access_token"]


def generate_password() -> tuple[str, str]:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    raw = f"{SHORTCODE}{PASSKEY}{timestamp}"
    password = base64.b64encode(raw.encode()).decode()
    return password, timestamp


class STKPushRequest(BaseModel):
    phone: str
    amount: int = 100
    description: str = "Buy Elijah a cup of tea"


class QRCodeRequest(BaseModel):
    amount: int = 100
    reference: str = "Tea for Elijah"


@router.post("/stk-push")
def stk_push(payload: STKPushRequest):
    # Normalize phone number to 254XXXXXXXXX
    phone = payload.phone.strip().replace(" ", "").replace("-", "")
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+"):
        phone = phone[1:]
    if not phone.startswith("254") or len(phone) != 12:
        raise HTTPException(status_code=400, detail="Invalid phone number. Use format: 07XXXXXXXX or 254XXXXXXXXX")

    if payload.amount < 1:
        raise HTTPException(status_code=400, detail="Amount must be at least KES 1")

    token = get_access_token()
    password, timestamp = generate_password()

    body = {
        "BusinessShortCode": SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": payload.amount,
        "PartyA": phone,
        "PartyB": SHORTCODE,
        "PhoneNumber": phone,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "ElijahKimani",
        "TransactionDesc": payload.description,
    }

    response = requests.post(
        f"{DARAJA_BASE}/mpesa/stkpush/v1/processrequest",
        json=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=20
    )

    data = response.json()
    if response.status_code != 200 or data.get("ResponseCode") != "0":
        error_msg = data.get("errorMessage") or data.get("ResponseDescription") or "STK Push failed"
        raise HTTPException(status_code=502, detail=error_msg)

    return {
        "success": True,
        "message": "STK Push sent! Check your phone for the M-Pesa prompt.",
        "checkout_request_id": data.get("CheckoutRequestID"),
        "merchant_request_id": data.get("MerchantRequestID"),
    }


@router.post("/qr-code")
def generate_qr(payload: QRCodeRequest):
    token = get_access_token()

    body = {
        "MerchantName": "Elijah Kimani",
        "RefNo": payload.reference,
        "Amount": payload.amount,
        "TrxCode": "PB",
        "CPI": SHORTCODE,
        "Size": "300",
    }

    response = requests.post(
        f"{DARAJA_BASE}/mpesa/qrcode/v1/generate",
        json=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=20
    )

    data = response.json()
    if response.status_code != 200 or data.get("ResponseCode") != "00":
        raise HTTPException(status_code=502, detail=data.get("ResponseDescription", "QR Code generation failed"))

    return {
        "success": True,
        "qr_code": data.get("QRCode"),
        "amount": payload.amount,
    }


@router.post("/callback")
async def mpesa_callback(data: dict):
    # Log callback data (in production, save to DB)
    print(f"M-Pesa Callback received: {data}")
    return {"ResultCode": 0, "ResultDesc": "Accepted"}
