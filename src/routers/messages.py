from fastapi import APIRouter, HTTPException
from src.config import settings
from src.utils import send_whatsapp_message
from src.models import TestMessageResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/test", response_model=TestMessageResponse)
async def send_test_message():
    """Send a test message to yourself"""
    try:
        result = send_whatsapp_message(
            settings.YOUR_PHONE_NUMBER, 
            "Hello from the bot! This is a test message."
        )
        return TestMessageResponse(
            status="success",
            message="Test message sent",
            response=result
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to send test message: {str(e)}"
        )

@router.post("/send")
async def send_custom_message(number: str, message: str):
    """Send a custom message to any number (for testing)"""
    try:
        result = send_whatsapp_message(number, message)
        return {
            "status": "success",
            "message": f"Message sent to {number}",
            "response": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send message: {str(e)}"
        )