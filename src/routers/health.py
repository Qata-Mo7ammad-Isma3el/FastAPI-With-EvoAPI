from fastapi import APIRouter, HTTPException
import json
import os
import requests
from src.config import settings
from src.models import HealthResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["Health"])

@router.get("/", response_model=HealthResponse)
async def health_check():
    """Check Evolution API connection and bot status"""
    try:
        # Check instance connection state
        url = f"{settings.EVOLUTION_API_URL}/instance/connectionState/{settings.INSTANCE_NAME}"
        response = requests.get(
            url, 
            headers=settings.evolution_headers, 
            timeout=10,
            verify=settings.SSL_VERIFY
        )
        state_info = response.json()
        
        return HealthResponse(
            status="healthy",
            bot="running",
            your_number=settings.YOUR_PHONE_NUMBER,
            evolution_api={
                "connected": True,
                "state": state_info.get("state"),
                "instance": settings.INSTANCE_NAME,
                "url": settings.EVOLUTION_API_URL
            },
            timestamp=json.dumps({"timestamp": os.times()}, default=str)
        )
    except Exception as e:
        return HealthResponse(
            status="partially_healthy",
            bot="running",
            your_number=settings.YOUR_PHONE_NUMBER,
            evolution_api={
                "connected": False,
                "error": str(e),
                "url": settings.EVOLUTION_API_URL
            },
            timestamp=json.dumps({"timestamp": os.times()}, default=str)
        )