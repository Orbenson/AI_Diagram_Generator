# src/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API keys for LLM integration
    google_api_key: Optional[str] = "AIzaSyAr_1zH1-NUtCMzfi5pReyCccsJqoaLV7g"
    huggingface_token: Optional[str] = None

    # LLM settings: primary Gemini model and fallback HuggingFace model
    gemini_model: str = "gemini-2.0-flash-001"
    hf_fallback_model: str = "distilgpt2"

    # Generation parameters
    temperature: float = 0.0

    # Logging level
    log_level: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
