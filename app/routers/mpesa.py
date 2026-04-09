from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import requests
import base64
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# ─────────────────────────────────────────────────────────────────────────────
# Environment toggle: set MPESA_ENV=production in Azure to switch to live mode
# ─────────────────────────────────────────────────────────────────────────────
MPESA_ENV = os.getenv("MPESA_ENV", "production")  # "sandbox" | "production"

if MPESA_ENV == "production":
    # Production credentials - CORRECTED from screenshot
    # Note: The key in the screenshot has 'DzqlxYK' (lowercase L) instead of 'DzqIxYK' (uppercase I)
    CONSUMER_KEY    = os.getenv("MPESA_CONSUMER_KEY",    "LM6MxKjJXDzqIxYK7ej1A6DWUd8sVJ6XYf22ByFh4R4rgykA")
    CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET", "MAjliohCqtGGvshySY8RkHZSF88eemW1Wp77PjwxO3ci0m7242fdGGEXv2TQkljk")
    PASSKEY         = os.getenv("MPESA_PASSKEY",         "d4f1dd629fbd7638a5272362f3b42057bf5fed09bca901db242b0ac7e88ee993")
    SHORTCODE       = os.getenv("MPESA_SHORTCODE",       "3538431")
    DARAJA_BASE     = "https://api.safaricom.co.ke"
else:
    # Sandbox mode
    CONSUMER_KEY    = "9v38Dtu5u2BpsITPmLcXNWGMsjZRWSTG"
    CONSUMER_SECRET = "bclwIPkcRqw61yUt"
    PASSKEY         = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    SHORTCODE       = "174379"
    DARAJA_BASE     = "https://sandbox.safaricom.co.ke"

CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL", "https://portifolio-ebdeg3d3fug9bffh.southafricanorth-01.azurewebsites.net/mpesa/callback")


def get_access_token() -> str:
    # Ensure we use the exact credentials
    credentials = base64.b64encode(f"{CONSUMER_KEY}:{CONSUMER_SECRET}".encode()).decode()
    url = f"{DARAJA_BASE}/oauth/v1/generate?grant_type=client_credentials"
    
    headers = {
        "Authorization": f"Basic {credentials}",
        "Accept": "application/json"
    }

    # Safaricom Production is sensitive to method and headers
    try:
        # Try GET first as it is the standard for Daraja token generation
        response = requests.get(url, headers=headers, timeout=30)
        
        # If GET fails or returns empty, try POST
        if response.status_code != 200 or not response.text.strip():
            logger.info(f"GET token failed (Status {response.status_code}), trying POST...")
            response = requests.post(url, headers=headers, timeout=30)
            
    except Exception as e:
        logger.error(f"Token request exception: {str(e)}")
        raise HTTPException(status_code=502, detail=f"M-Pesa connection error: {str(e)}")

    if response.status_code != 200:
        logger.error(f"Failed to get token. Status: {response.status_code}, Response: {response.text}")
        raise HTTPException(
            status_code=502,
            detail=f"M-Pesa Auth Failed (HTTP {response.status_code}). Please check Consumer Key/Secret."
        )

    try:
        data = response.json()
        token = data.get("access_token")
        if not token:
            logger.error(f"Token missing in JSON: {data}")
            raise HTTPException(status_code=502, detail="Access token missing from Daraja response.")
        return token
    except Exception:
        logger.error(f"Invalid JSON response: {response.text}")
        raise HTTPException(status_code=502, detail="Daraja API returned an unexpected response format.")


def generate_password() -> tuple[str, str]:
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    raw = f"{SHORTCODE}{PASSKEY}{timestamp}"
    password = base64.b64encode(raw.encode()).decode()
    return password, timestamp


class STKPushRequest(BaseModel):
    phone_number: str
    amount: int = 100
    description: str = "Buy Elijah a cup of tea"


@router.post("/stk-push")
def stk_push(payload: STKPushRequest):
    # Normalize phone number to 254XXXXXXXXX
    phone = payload.phone_number.strip().replace(" ", "").replace("-", "")
    if phone.startswith("0"):
        phone = "254" + phone[1:]
    elif phone.startswith("+"):
        phone = phone[1:]

    if not phone.startswith("254") or len(phone) != 12:
        raise HTTPException(
            status_code=400,
            detail="Invalid phone number. Use format: 07XXXXXXXX or 254XXXXXXXXX"
        )

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

    logger.info(f"Sending STK Push to {phone} for amount {payload.amount}")
    
    response = requests.post(
        f"{DARAJA_BASE}/mpesa/stkpush/v1/processrequest",
        json=body,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        timeout=30
    )

    try:
        data = response.json()
    except Exception:
        logger.error(f"Invalid JSON from M-Pesa STK: {response.text}")
        raise HTTPException(status_code=502, detail="Invalid response from M-Pesa STK Push API")

    if response.status_code != 200 or data.get("ResponseCode") != "0":
        error_msg = (
            data.get("errorMessage")
            or data.get("ResponseDescription")
            or data.get("errorCode")
            or "STK Push failed"
        )
        logger.error(f"STK Push failed: {error_msg}")
        raise HTTPException(status_code=502, detail=error_msg)

    return {
        "success": True,
        "message": "STK Push sent! Check your phone for the M-Pesa prompt.",
        "checkout_request_id": data.get("CheckoutRequestID"),
        "merchant_request_id": data.get("MerchantRequestID"),
        "environment": MPESA_ENV,
    }


@router.post("/callback")
async def mpesa_callback(request: Request):
    try:
        data = await request.json()
        logger.info(f"M-Pesa Callback received: {data}")
        
        stk_callback = data.get("Body", {}).get("stkCallback", {})
        result_code = stk_callback.get("ResultCode")
        result_desc = stk_callback.get("ResultDesc")
        checkout_id = stk_callback.get("CheckoutRequestID")
        
        logger.info(f"Transaction {checkout_id} result: {result_code} - {result_desc}")
        
        return {"ResultCode": 0, "ResultDesc": "Accepted"}
    except Exception as e:
        logger.error(f"Error processing callback: {str(e)}")
        return {"ResultCode": 1, "ResultDesc": "Error processing callback"}
