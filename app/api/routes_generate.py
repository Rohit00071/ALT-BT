"""
API route for video generation.
POST /api/generate_video
"""

import logging
from fastapi import APIRouter

from app.models.dto import GenerateRequest, GenerateResponse
from app.services.llm_client import generate_manim_code
from app.services.sanitizer import sanitize_code
from app.services.manim_runner import render_scene

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/api/generate_video", response_model=GenerateResponse)
async def generate_video(request: GenerateRequest):
    """
    Generate an educational Manim animation video.

    1. Validate input.
    2. Generate Manim code via LLM.
    3. Sanitize the generated code.
    4. Render the scene with Manim CLI.
    5. Return the video URL.
    """
    concept = request.concept.strip()
    language = request.language.strip() if request.language else "English"

    if not concept:
        return GenerateResponse(
            status="error",
            message="Please enter a math concept.",
        )

    logger.info(f"Generating video: concept='{concept}', language='{language}'")

    # Step 1: Generate Manim code using LLM
    try:
        raw_code = generate_manim_code(concept, language)
    except ValueError as e:
        logger.error(f"LLM config error: {e}")
        return GenerateResponse(
            status="error",
            message="AI service is not configured properly. Check your API keys.",
            details=str(e),
        )
    except Exception as e:
        logger.error(f"LLM generation failed: {e}")
        return GenerateResponse(
            status="error",
            message="AI failed to generate animation code. Please try again.",
            details=str(e)[:300],
        )

    # Step 2: Sanitize the generated code
    try:
        clean_code = sanitize_code(raw_code)
    except ValueError as e:
        logger.warning(f"Sanitization rejected code: {e}")
        return GenerateResponse(
            status="error",
            message="The AI generated unsafe or invalid code. Please try a different concept.",
            details=str(e)[:300],
        )

    # Step 3: Render with Manim
    try:
        video_url = render_scene(clean_code)
    except TimeoutError as e:
        return GenerateResponse(
            status="error",
            message=str(e),
        )
    except RuntimeError as e:
        return GenerateResponse(
            status="error",
            message="AI generated invalid Manim code. Please try a different prompt.",
            details=str(e)[:500],
        )
    except Exception as e:
        logger.error(f"Unexpected render error: {e}")
        return GenerateResponse(
            status="error",
            message="An unexpected error occurred during rendering.",
            details=str(e)[:300],
        )

    logger.info(f"Video generated successfully: {video_url}")
    return GenerateResponse(
        status="success",
        video_url=video_url,
        message="Video generated successfully!",
    )
