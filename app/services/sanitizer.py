"""
Code sanitizer — cleans and validates LLM-generated Manim code.
"""

import re
import logging

logger = logging.getLogger(__name__)

# Dangerous imports that must NOT appear in generated code
FORBIDDEN_IMPORTS = [
    r"\bimport\s+os\b",
    r"\bfrom\s+os\b",
    r"\bimport\s+sys\b",
    r"\bfrom\s+sys\b",
    r"\bimport\s+subprocess\b",
    r"\bfrom\s+subprocess\b",
    r"\bimport\s+socket\b",
    r"\bfrom\s+socket\b",
    r"\bimport\s+requests\b",
    r"\bfrom\s+requests\b",
    r"\bimport\s+urllib\b",
    r"\bfrom\s+urllib\b",
    r"\bimport\s+shutil\b",
    r"\bfrom\s+shutil\b",
    r"\bimport\s+pathlib\b",
    r"\bfrom\s+pathlib\b",
    r"\b__import__\b",
    r"\beval\s*\(",
    r"\bexec\s*\(",
    r"\bopen\s*\(",
]


def sanitize_code(raw_code: str) -> str:
    """
    Clean and validate LLM-generated Manim code.

    Steps:
    1. Strip markdown code fences if present.
    2. Trim whitespace.
    3. Check for forbidden imports/calls.
    4. Verify GeneratedScene class exists.

    Args:
        raw_code: The raw string returned by the LLM.

    Returns:
        Cleaned Python code string.

    Raises:
        ValueError: If the code contains forbidden patterns or is missing GeneratedScene.
    """
    code = raw_code.strip()

    # Strip markdown fences
    # Match ```python ... ``` or ``` ... ```
    fence_pattern = r"^```(?:python)?\s*\n?(.*?)```\s*$"
    match = re.match(fence_pattern, code, re.DOTALL)
    if match:
        code = match.group(1).strip()

    # Also strip any leading/trailing backticks that might remain
    code = code.strip("`").strip()

    # Check for forbidden imports and calls
    for pattern in FORBIDDEN_IMPORTS:
        if re.search(pattern, code):
            raise ValueError(
                f"Generated code contains forbidden pattern: {pattern}. "
                "Please try a different concept."
            )

    # Verify the scene class exists
    if "class GeneratedScene" not in code:
        # Try to find any Scene subclass and rename it
        scene_match = re.search(r"class\s+(\w+)\s*\(\s*Scene\s*\)", code)
        if scene_match:
            original_name = scene_match.group(1)
            code = code.replace(f"class {original_name}(Scene)", "class GeneratedScene(Scene)")
            logger.info(f"Renamed scene class '{original_name}' to 'GeneratedScene'")
        else:
            raise ValueError(
                "Generated code does not contain a valid Scene class. "
                "The AI may have produced invalid output. Please try again."
            )

    # Ensure it has the manim import
    if "from manim import" not in code and "import manim" not in code:
        code = "from manim import *\n\n" + code

    # Failsafe: Replace MathTex and Tex with Text since LaTeX is not installed
    # These often cause rendering to hang or fail silently if LaTeX is missing
    code = code.replace("MathTex(", "Text(").replace("Tex(", "Text(")

    # Failsafe: Remove wrap_width from Text() calls as it's not supported by manim's Text class
    code = re.sub(r"Text\((.*)\s*,\s*wrap_width\s*=\s*[^,)]*", r"Text(\1", code)

    return code
