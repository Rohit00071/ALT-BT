"""
Application configuration using Pydantic BaseSettings.
All values can be overridden via environment variables or a .env file.
"""

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application settings — all providers are FREE-TIER ONLY."""

    # LLM Provider: "gemini" or "groq"
    LLM_PROVIDER: str = Field(default="gemini", description="LLM provider to use")

    # Google Gemini (free tier)
    GEMINI_API_KEY: str = Field(default="", description="Gemini API key (free tier)")
    GEMINI_MODEL_NAME: str = Field(default="gemini-2.0-flash", description="Gemini model name")

    # Groq (free tier)
    GROQ_API_KEY: str = Field(default="", description="Groq API key (free tier)")
    GROQ_MODEL_NAME: str = Field(default="llama-3.3-70b-versatile", description="Groq model name")

    # Rendering paths
    VIDEO_OUTPUT_DIR: str = Field(default="./videos", description="Directory for rendered MP4s")
    TEMP_SCENE_DIR: str = Field(default="./tmp_scenes", description="Directory for temp .py files")

    # Font for non-Latin scripts
    NON_LATIN_FONT_NAME: str = Field(default="Noto Sans", description="Font for non-Latin text")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True,
    }


# Singleton instance
settings = Settings()
