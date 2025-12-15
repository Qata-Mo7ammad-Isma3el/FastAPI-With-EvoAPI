from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from src.config import settings
from src.routers import webhook, health, messages, debug  # Add debug import

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan context manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("=" * 60)
    logger.info(f"🚀 Starting WhatsApp Bot")
    logger.info(f"📱 Your WhatsApp number: {settings.YOUR_PHONE_NUMBER}")
    logger.info(f"🔗 Evolution API URL: {settings.EVOLUTION_API_URL}")
    logger.info(f"🏷️  Instance name: {settings.INSTANCE_NAME}")
    logger.info(f"🌐 Bot running on: http://localhost:{settings.PORT}")
    logger.info("=" * 60)
    
    yield  # This is where the app runs
    
    # Shutdown logic
    logger.info("=" * 60)
    logger.info("🛑 Shutting down WhatsApp Bot")
    logger.info("=" * 60)

# Initialize FastAPI with lifespan
app = FastAPI(
    title="WhatsApp Bot",
    description="Simple WhatsApp bot using Evolution API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(messages.router, tags=["Messages"])
app.include_router(webhook.router, tags=["Webhook"])
#> app.include_router(debug.router, tags=["Debug"])  # Add debug router

# Root endpoint
@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "WhatsApp Bot API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "health": "/health",
            "test_message": "/messages/test",
            "webhook": "/webhook",
            "debug": "/debug/config"
        }
    }