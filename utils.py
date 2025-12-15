from fastapi import FastAPI, Request, HTTPException
import requests
import json
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)
# Configuration
YOUR_NUMBER = os.getenv("YOUR_PHONE_NUMBER", "+962787499976")
EVOLUTION_API_URL = os.getenv("EVOLUTION_API_URL", "http://localhost:8080")
EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY")
INSTANCE_NAME = os.getenv("INSTANCE_NAME", "evolution_api")

# Headers for Evolution API
EVOLUTION_HEADERS = {
    "apikey": EVOLUTION_API_KEY,
}

def clean_phone_number(phone: str) -> str:
    """Clean phone number by removing + and @s.whatsapp.net"""
    # Remove + sign and @s.whatsapp.net suffix
    clean = phone.replace('+', '')
    if '@s.whatsapp.net' in clean:
        clean = clean.split('@')[0]
    return clean

def is_my_number(sender_jid: str) -> bool:
    """Check if sender is your phone number"""
    clean_sender = clean_phone_number(sender_jid)
    clean_my_number = clean_phone_number(YOUR_NUMBER)
    return clean_sender == clean_my_number

def send_whatsapp_message(phone_number: str, text: str):
    """
    Send WhatsApp message using Evolution API format
    POST https://{server-url}/message/sendText/{instance}
    """
    url = f"{EVOLUTION_API_URL}/message/sendText/{INSTANCE_NAME}"
    
    # Clean the phone number
    clean_number = clean_phone_number(phone_number)
    
    # Prepare payload according to Evolution API format
    payload = {
        "number": clean_number,
        "textMessage": {
            "text": text
        },
        "options": {
            "delay": 1000,  # 1 second delay
            "presence": "composing",
            "linkPreview": False
        }
    }
    
    logger.info(f"Sending message to {clean_number}: {text}")
    
    try:
        response = requests.post(
            url,
            json=payload,
            headers=EVOLUTION_HEADERS,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f"Message sent successfully: {result}")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message: {str(e)}")
        if hasattr(e, 'response') and e.response is not None:
            logger.error(f"Response content: {e.response.text}")
        raise
