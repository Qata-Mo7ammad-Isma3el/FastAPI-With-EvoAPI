import requests
import logging
from typing import Dict, Any
from groq import Groq
from src.config import settings

logger = logging.getLogger(__name__)


def clean_phone_number(phone: str) -> str:
    """Clean phone number by removing + and @s.whatsapp.net"""
    clean = phone.replace("+", "")
    if "@s.whatsapp.net" in clean:
        clean = clean.split("@")[0]
    return clean


def is_my_number(sender_jid: str) -> bool:
    """Check if sender is your phone number"""
    clean_sender = clean_phone_number(sender_jid)
    clean_my_number = clean_phone_number(settings.YOUR_PHONE_NUMBER)
    return clean_sender == clean_my_number


def send_whatsapp_message(phone_number: str, text: str) -> Dict[str, Any]:
    """
    Send WhatsApp message using Evolution API format
    POST https://{server-url}/message/sendText/{instance}
    """
    # Ensure URL doesn't have double slashes
    base_url = settings.EVOLUTION_API_URL.rstrip("/")
    url = f"{base_url}/message/sendText/{settings.INSTANCE_NAME}"

    # Clean the phone number
    clean_number = clean_phone_number(phone_number)

    # Prepare payload according to Evolution API format
    payload = {
        "number": clean_number,
        "text": text,
        "options": {"delay": 1000, "presence": "composing", "linkPreview": False},
    }
    try:
        response = requests.post(
            url,
            json=payload,
            headers=settings.evolution_headers,
            timeout=30,
            verify=settings.SSL_VERIFY,
        )
        response.raise_for_status()
        result = response.json()
        logger.info(f"Message sent successfully")
        return result
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send message: {str(e)}")
        if hasattr(e, "response") and e.response is not None:
            logger.error(f"Response status: {e.response.status_code}")
            logger.error(f"Response content: {e.response.text}")
        raise

def get_llm_response(user_message: str) -> str:
    """
    Get response from Groq LLM
    """
    try:
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful WhatsApp assistant. Keep responses concise and friendly. Do not include any thinking process or internal reasoning in your response."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            model=settings.GROQ_MODEL,
            temperature=0.7,
            max_tokens=500,
        )
        
        return chat_completion.choices[0].message.content
    except Exception as e:
        logger.error(f"❌ Groq API error: {e}")
        return "Sorry, I couldn't process your message right now."
