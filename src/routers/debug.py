from fastapi import APIRouter, HTTPException
import requests
import logging
from src.config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/test-connection")
async def test_evolution_connection():
    """Test Evolution API connection directly"""
    try:
        base_url = settings.EVOLUTION_API_URL.rstrip("/")
        url = f"{base_url}/instance/connectionState/{settings.INSTANCE_NAME}"

        logger.info(f"Testing connection to: {url}")

        response = requests.get(
            url,
            headers=settings.evolution_headers,
            timeout=10,
            verify=settings.SSL_VERIFY,
        )

        return {
            "url": url,
            "status_code": response.status_code,
            "response": (
                response.json() if response.status_code == 200 else response.text
            ),
            "headers_sent": {"apikey": "***" if settings.EVOLUTION_API_KEY else "None"},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/test-send")
async def test_send_message():
    """Test sending a message with detailed logging"""
    try:
        from src.utils import send_whatsapp_message

        result = send_whatsapp_message(
            settings.YOUR_PHONE_NUMBER, "Test message from debug endpoint"
        )

        return {"status": "success", "message": "Test message sent", "result": result}
    except Exception as e:
        import traceback

        return {"status": "error", "error": str(e), "traceback": traceback.format_exc()}


@router.get("/config")
async def show_config():
    """Show current configuration (without sensitive data)"""
    return {
        "YOUR_PHONE_NUMBER": settings.YOUR_PHONE_NUMBER,
        "EVOLUTION_API_URL": settings.EVOLUTION_API_URL,
        "INSTANCE_NAME": settings.INSTANCE_NAME,
        "BOT_URL": settings.BOT_URL,
        "PORT": settings.PORT,
        "SSL_VERIFY": settings.SSL_VERIFY,
        "EVOLUTION_API_KEY_SET": bool(settings.EVOLUTION_API_KEY),
        "evolution_headers": {
            "apikey": settings.EVOLUTION_API_KEY,
            "Content-Type": "application/json",
        },
    }


@router.get("/test-api-key")
async def test_api_key():
    """Test if API key is working"""
    try:
        base_url = settings.EVOLUTION_API_URL.rstrip("/")

        url = f"{base_url}/instance/fetchInstances"

        logger.info(f"Testing API key with URL: {url}")
        logger.info(
            f"API key length: {len(settings.EVOLUTION_API_KEY) if settings.EVOLUTION_API_KEY else 0}"
        )

        # Show first few characters of API key (for debugging, remove in production)
        if settings.EVOLUTION_API_KEY:
            masked_key = (
                settings.EVOLUTION_API_KEY[:8] + "..." + settings.EVOLUTION_API_KEY[-4:]
                if len(settings.EVOLUTION_API_KEY) > 12
                else "***"
            )
            logger.info(f"API key (masked): {masked_key}")

        # Log actual headers being sent
        actual_headers = settings.evolution_headers.copy()
        print(actual_headers)  # For immediate visibility in console
        logger.info(f"Headers being sent: {actual_headers}")

        response = requests.get(
            url,
            headers=actual_headers,
            timeout=10,
            verify=settings.SSL_VERIFY,
        )

        # Also check what the server received
        logger.info(f"Response status: {response.status_code}")
        logger.info(f"Response headers: {dict(response.headers)}")

        return {
            "url": url,
            "status_code": response.status_code,
            "response": (
                response.json() if response.status_code == 200 else response.text
            ),
            "headers_sent": actual_headers,
            "response_headers": dict(response.headers),
            "actual_apikey_length": (
                len(settings.EVOLUTION_API_KEY) if settings.EVOLUTION_API_KEY else 0
            ),
        }
    except Exception as e:
        import traceback

        return {
            "error": str(e),
            "traceback": traceback.format_exc(),
            "config_check": {
                "EVOLUTION_API_URL": settings.EVOLUTION_API_URL,
                "INSTANCE_NAME": settings.INSTANCE_NAME,
                "API_KEY_SET": bool(settings.EVOLUTION_API_KEY),
            },
        }


@router.get("/test-headers")
async def test_different_headers():
    """Test different header variations to find the correct format"""
    base_url = settings.EVOLUTION_API_URL.rstrip("/")
    url = f"{base_url}/instance/fetchInstances"

    results = []

    # Test different header variations
    header_variations = [
        {"apikey": settings.EVOLUTION_API_KEY, "Content-Type": "application/json"},
        {"apiKey": settings.EVOLUTION_API_KEY, "Content-Type": "application/json"},
        {"API-KEY": settings.EVOLUTION_API_KEY, "Content-Type": "application/json"},
        {"Api-Key": settings.EVOLUTION_API_KEY, "Content-Type": "application/json"},
        {
            "Authorization": f"Bearer {settings.EVOLUTION_API_KEY}",
            "Content-Type": "application/json",
        },
    ]

    for i, headers in enumerate(header_variations):
        try:
            response = requests.get(
                url, headers=headers, timeout=10, verify=settings.SSL_VERIFY
            )
            header_name = list(headers.keys())[0]  # Get first key name
            results.append(
                {
                    "attempt": i + 1,
                    "header_name": header_name,
                    "status_code": response.status_code,
                    "success": response.status_code == 200,
                    "response": (
                        response.text[:200]
                        if response.status_code != 200
                        else "Success!"
                    ),
                }
            )
        except Exception as e:
            results.append({"attempt": i + 1, "error": str(e)})

    return {"url": url, "tests": results}
