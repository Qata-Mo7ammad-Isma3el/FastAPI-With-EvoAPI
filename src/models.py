from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class WhatsAppMessage(BaseModel):
    number: str
    textMessage: Dict[str, Any] = Field(default_factory=lambda: {"text": ""})
    options: Optional[Dict[str, Any]] = Field(default_factory=lambda: {
        "delay": 1000,
        "presence": "composing",
        "linkPreview": False
    })

class WebhookPayload(BaseModel):
    event: str
    instance: str
    data: Dict[str, Any]

class HealthResponse(BaseModel):
    status: str
    bot: str
    your_number: str
    evolution_api: Dict[str, Any]
    timestamp: str

class TestMessageResponse(BaseModel):
    status: str
    message: str
    response: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class WebhookResponse(BaseModel):
    status: str
    message: str
    your_number: str