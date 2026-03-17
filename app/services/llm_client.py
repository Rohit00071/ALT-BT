"""
LLM client abstraction — pluggable provider via LLM_PROVIDER env var.
Builds the strict Manim prompt and delegates to the correct client.
"""

import logging
from app.core.config import settings
from app.services.gemini_client import generate_code_gemini
from app.services.groq_client import generate_code_groq

logger = logging.getLogger(__name__)

# Languages that need a non-Latin font
NON_LATIN_LANGUAGES = {
    "hindi", "arabic", "japanese", "chinese", "korean", "thai", "tamil",
    "telugu", "bengali", "gujarati", "kannada", "malayalam", "marathi",
    "punjabi", "urdu", "persian", "hebrew", "nepali", "sinhala",
    "russian", "ukrainian", "greek", "georgian", "armenian",
}


def _build_prompt(concept: str, language: str) -> str:
    """Construct a strict prompt for Manim code generation."""
    font_name = settings.NON_LATIN_FONT_NAME
    is_non_latin = language.lower() in NON_LATIN_LANGUAGES

    font_instruction = ""
    if is_non_latin:
        font_instruction = f"""
CRITICAL FONT REQUIREMENT:
- The target language is "{language}" which uses a non-Latin script.
- For ALL Text() objects, you MUST set font="{font_name}".
  Example: Text("your text here", font="{font_name}")
- Do NOT use Tex() or MathTex() for non-Latin text. Use Text() with the font parameter.
- For mathematical expressions, you can still use MathTex().
"""

    prompt = f"""Generate a Manim Community Edition Python script that creates an educational animation
explaining the mathematical concept: "{concept}".

All on-screen text labels and titles MUST be written in {language}.

STRICT RULES — follow every single one:
1. Output ONLY raw Python code. No markdown fences, no backticks, no explanations before or after the code.
2. Use Manim Community Edition imports: from manim import *
3. Define EXACTLY ONE scene class named GeneratedScene that inherits from Scene.
4. The class must have a construct(self) method.
5. Do NOT import os, sys, subprocess, socket, requests, urllib, or any network/file I/O library.
6. Do NOT read or write any files.
7. Use simple, reliable Manim animations: Write, FadeIn, FadeOut, Create, Transform, MoveToTarget, etc.
8. Keep the animation short (15-30 seconds of content), clear, and educational.
9. Use colors to make the animation visually appealing.
10. Add a title at the beginning and a summary/conclusion at the end.
11. Make sure all objects are properly positioned and don't overlap.
12. Use self.play() for animations and self.wait() for pauses.
13. Clean up objects with FadeOut or self.remove() before adding new ones to avoid clutter.
14. CRITICAL: LaTeX IS NOT INSTALLED. You MUST NOT use Tex() or MathTex().
15. Use Text() for ALL text, including mathematical formulas. For exponents or special symbols, use standard Unicode or plain text (e.g., Text("a^2 + b^2 = c^2")).
16. Do NOT use wrap_width in Text(). If text is too long, use multiple Text objects or keep it short.
{font_instruction}
Remember: Output ONLY the Python code. Nothing else. No explanations. No markdown.
Start directly with 'from manim import *'.
"""
    return prompt.strip()


def generate_manim_code(concept: str, language: str) -> str:
    """
    Generate Manim scene code using the configured LLM provider.

    Args:
        concept: The math concept to animate.
        language: The language for on-screen text.

    Returns:
        Raw Python code string for a Manim scene.

    Raises:
        ValueError: If the provider is not configured or API key is missing.
        RuntimeError: If the LLM returns an empty or invalid response.
    """
    prompt = _build_prompt(concept, language)
    provider = settings.LLM_PROVIDER.lower()

    logger.info(f"Generating Manim code with provider: {provider}")

    if provider == "gemini":
        return generate_code_gemini(prompt)
    elif provider == "groq":
        return generate_code_groq(prompt)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: '{provider}'. Use 'gemini' or 'groq'.")
