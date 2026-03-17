"""
Groq client — uses Groq Python SDK (free tier, no credit card).
"""

import logging
from groq import Groq
from app.core.config import settings

logger = logging.getLogger(__name__)


def generate_code_groq(prompt: str) -> str:
    """Call Groq free-tier model and return the text response."""
    api_key = settings.GROQ_API_KEY
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set. Please configure it in your .env file.")

    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are a Manim code generator. Output ONLY raw Python code. No markdown, no explanations.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model=settings.GROQ_MODEL_NAME,
        temperature=0.3,
        max_tokens=4096,
    )

    text = chat_completion.choices[0].message.content
    if not text:
        raise RuntimeError("Groq returned an empty response.")

    return text.strip()
