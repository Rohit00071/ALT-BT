import os
import sys
from dotenv import load_dotenv

# Add the current directory to sys.path to import app
sys.path.append(os.getcwd())

from app.services.llm_client import generate_manim_code
from app.services.sanitizer import sanitize_code
from app.services.manim_runner import render_scene

load_dotenv()

# Ensure terminal output supports Unicode (for square root symbols, etc.)
if sys.stdout.encoding.lower() != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_generation(concept, language="English"):
    print(f"\n--- Testing: {concept} ({language}) ---")
    try:
        print("Generating code...")
        raw_code = generate_manim_code(concept, language)
        print("\n--- RAW CODE START ---")
        print(raw_code)
        print("--- RAW CODE END ---\n")

        print("Sanitizing code...")
        clean_code = sanitize_code(raw_code)
        print("\n--- CLEAN CODE START ---")
        print(clean_code)
        print("--- CLEAN CODE END ---\n")

        print("Rendering scene...")
        video_url = render_scene(clean_code)
        print(f"Success! Video URL: {video_url}")

    except Exception as e:
        print(f"Error occurred: {type(e).__name__}: {e}")

if __name__ == "__main__":
    # Test with a simple concept that might have failed
    test_generation("Pythagorean Theorem")
