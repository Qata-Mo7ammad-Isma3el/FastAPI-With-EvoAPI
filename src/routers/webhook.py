from fastapi import APIRouter, Request, HTTPException
import json
import logging
from src.config import settings
from src.utils import is_my_number, send_whatsapp_message, get_llm_response
from src.models import WebhookResponse
import re

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhook", tags=["Webhook"])

# logger.info(f"📨 Received webhook event: {event_type}")
# # Log the full payload for debugging
# logger.info(f"📋 Full webhook data: {json.dumps(webhook_data, indent=2)}")


@router.post("/messages-upsert", response_model=WebhookResponse)
async def webhook_handler(request: Request):
    """
    Webhook endpoint for Evolution API messages
    Processes incoming WhatsApp messages and sends auto-reply
    """
    try:
        # Parse webhook payload
        webhook_data = await request.json()
        event_type = webhook_data.get("event")

        logger.info(f"📨 Event: {event_type}")

        # Process message upsert events
        if event_type == "messages.upsert":
            data = webhook_data.get("data", {})

            # Extract message details
            key = data.get("key", {})
            sender_jid = key.get("remoteJid", "")
            from_me = key.get("fromMe", False)
            push_name = data.get("pushName", "Unknown")

            # # Skip messages sent by the bot
            # if from_me:
            #     logger.info("⏭️  Skipping outgoing message")
            #     return WebhookResponse(
            #         status="success",
            #         message="Skipped outgoing message",
            #         your_number=settings.YOUR_PHONE_NUMBER,
            #     )

            # Extract message text
            message_data = data.get("message", {})
            text = message_data.get("conversation") or message_data.get(
                "extendedTextMessage", {}
            ).get("text")

            if text and is_my_number(sender_jid):
                logger.info(f"💬 From: {push_name} ({sender_jid})")
                logger.info(f"📝 Message: {text}")

                # Get LLM response
                logger.info("🤖 Generating AI response...")
                response_text = get_llm_response(text)
                cleaned_response = re.sub(
                    r"<think>.*?</think>", "", response_text, flags=re.DOTALL
                )

                # Remove <prompt> tags if present
                cleaned_response = re.sub(
                    r"<prompt>.*?</prompt>", "", cleaned_response, flags=re.DOTALL
                )

                # Clean up extra whitespace
                cleaned_response = cleaned_response.strip()
                logger.info(f"💡 AI Response: {response_text}")

                try:
                    # logger.info(f"📤 Sending reply: {response_text}")
                    result = send_whatsapp_message(sender_jid, cleaned_response)
                    logger.info(f"✅ Reply sent successfully!")
                except Exception as e:
                    logger.error(f"❌ Failed to send reply: {e}")
                    import traceback

                    logger.error(traceback.format_exc())

        # Return success response
        return WebhookResponse(
            status="success",
            message="Webhook processed",
            your_number=settings.YOUR_PHONE_NUMBER,
        )

    except json.JSONDecodeError:
        logger.error("❌ Invalid JSON in webhook")
        return WebhookResponse(
            status="error",
            message="Invalid JSON",
            your_number=settings.YOUR_PHONE_NUMBER,
        )
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        import traceback

        logger.error(traceback.format_exc())
        return WebhookResponse(
            status="error", message=str(e), your_number=settings.YOUR_PHONE_NUMBER
        )
