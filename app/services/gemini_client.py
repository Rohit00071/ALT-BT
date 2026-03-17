"""
Gemini client — uses Google GenAI SDK (free tier).
Includes retry logic and model fallback for rate limits.
"""

import logging
import time
from google import genai
from app.core.config import settings

logger = logging.getLogger(__name__)

# Fallback models to try if the primary model hits rate limits
FALLBACK_MODELS = [
    "gemini-1.5-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash",
]


def generate_code_gemini(prompt: str) -> str:
    """Call Gemini free-tier model and return the text response.
    Retries with fallback models if rate-limited."""
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Please configure it in your .env file.")

    client = genai.Client(api_key=api_key)

    # Build list of models to try: configured model first, then fallbacks
    models_to_try = [settings.GEMINI_MODEL_NAME]
    for m in FALLBACK_MODELS:
        if m not in models_to_try:
            models_to_try.append(m)

    last_error = None
    for model_name in models_to_try:
        try:
            logger.info(f"Trying Gemini model: {model_name}")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )

            if not response.text:
                raise RuntimeError(f"Gemini ({model_name}) returned an empty response.")

            logger.info(f"Successfully generated code with model: {model_name}")
            return response.text.strip()

        except Exception as e:
            error_str = str(e)
            last_error = e
            if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                logger.warning(f"Rate limited on {model_name}, trying next model...")
                time.sleep(2)  # Brief pause before trying next model
                continue
            else:
                # Non-rate-limit error, raise immediately
                raise

    # All models exhausted
    raise RuntimeError(
        f"All Gemini models are rate-limited. Please wait a minute and try again. "
        f"Last error: {last_error}"
    )
