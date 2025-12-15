from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # GROQ API Configuration
    GROQ_API_KEY: str
    GROQ_MODEL: str = "llama-3.3-70b-versatile"  # or mixtral-8x7b-32768
    
    # Your phone number
    YOUR_PHONE_NUMBER: str = "+962787499976"

    # Evolution API Configuration
    EVOLUTION_API_URL: str = "http://localhost:8080"
    EVOLUTION_API_KEY: str 
    INSTANCE_NAME: str = "evolution_api"

    # Bot Configuration
    BOT_URL: str = "http://localhost:8000"
    PORT: int = 8000

    # SSL Configuration
    SSL_VERIFY: bool = True

    # Headers for Evolution API
    @property
    def evolution_headers(self):
        return {"apikey": self.EVOLUTION_API_KEY, "Content-Type": "application/json"}

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore"
    )


# Global settings instance
settings = Settings()
