"""
Manim runner — writes temp scene files and invokes Manim CLI via subprocess.
"""

import subprocess
import uuid
import logging
from pathlib import Path

from app.core.config import settings

logger = logging.getLogger(__name__)

# Timeout for Manim rendering (seconds)
RENDER_TIMEOUT = 120


def render_scene(code: str) -> str:
    """
    Write Manim scene code to a temp file and render it to MP4.

    Args:
        code: Sanitized Python code containing a GeneratedScene class.

    Returns:
        Relative URL path to the rendered MP4 (e.g., "/videos/abc123_output.mp4").

    Raises:
        TimeoutError: If rendering exceeds the timeout.
        RuntimeError: If Manim exits with a non-zero return code.
    """
    scene_dir = Path(settings.TEMP_SCENE_DIR)
    video_dir = Path(settings.VIDEO_OUTPUT_DIR)

    # Create directories if they don't exist
    scene_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)

    # Generate unique ID for this render
    render_id = uuid.uuid4().hex[:12]
    scene_filename = f"{render_id}_scene.py"
    output_filename = f"{render_id}_output.mp4"
    scene_file = scene_dir / scene_filename

    # Write the scene code to a temp file
    scene_file.write_text(code, encoding="utf-8")
    logger.info(f"Wrote scene to: {scene_file}")

    # Build the Manim command
    # -ql = low quality (480p) for fast rendering
    # --media_dir = output directory
    # -o = output filename
    # The manim executable might not be in the PATH when running via subprocess on Windows.
    # We use the absolute path confirmed on this system.
    manim_cmd = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Python\\Python312\\Scripts\\manim.EXE"
    
    cmd = [
        manim_cmd,
        "-ql",
        str(scene_file),
        "GeneratedScene",
        "--media_dir", str(video_dir),
        "-o", output_filename,
    ]

    logger.info(f"Running Manim: {' '.join(cmd)}")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=RENDER_TIMEOUT,
            cwd=str(Path.cwd()),
        )
    except FileNotFoundError:
        logger.error(f"Manim executable not found at: {manim_cmd}")
        # Fallback to just "manim" if the absolute path fails
        try:
            logger.info("Retrying with 'manim' via shell...")
            result = subprocess.run(
                ["manim"] + cmd[1:],
                capture_output=True,
                text=True,
                timeout=RENDER_TIMEOUT,
                cwd=str(Path.cwd()),
                shell=True
            )
        except Exception as e:
            raise RuntimeError(f"Could not execute Manim: {e}")
    except subprocess.TimeoutExpired:
        logger.error(f"Manim render timed out after {RENDER_TIMEOUT}s")
        # Clean up temp file
        _cleanup(scene_file)
        raise TimeoutError(
            "Rendering took too long. Try a simpler or shorter concept."
        )

    if result.returncode != 0:
        stderr_snippet = (result.stderr or "")[-2000:] # Get the END of stderr for traceback
        logger.error(f"Manim failed (rc={result.returncode}): {stderr_snippet}")
        # _cleanup(scene_file)
        raise RuntimeError(
            f"Manim rendering failed. The AI may have generated invalid code. "
            f"Details: {stderr_snippet}"
        )

    # Find the actual output video file
    # Manim outputs to: media_dir/videos/<scene_filename_without_ext>/480p15/<output>.mp4
    scene_stem = scene_file.stem
    search_dir = video_dir / "videos"
    video_path = _find_video(search_dir, output_filename)

    if video_path is None:
        # Try alternative paths
        video_path = _find_video(video_dir, output_filename)

    if video_path is None:
        logger.error(f"Could not find output video. Manim stdout: {result.stdout[:300]}")
        logger.error(f"Searching in: {video_dir}")
        # List what's there for debugging
        _log_directory_tree(video_dir)
        raise RuntimeError("Video was rendered but the output file could not be located.")

    # Copy the video to the root videos directory for easy serving
    final_path = video_dir / output_filename
    if video_path != final_path:
        import shutil
        shutil.copy2(str(video_path), str(final_path))

    logger.info(f"Video ready at: {final_path}")

    # Clean up temp scene file
    # _cleanup(scene_file)

    return f"/videos/{output_filename}"


def _find_video(search_dir: Path, filename: str) -> Path | None:
    """Recursively search for a video file in a directory."""
    if not search_dir.exists():
        return None
    for path in search_dir.rglob(filename):
        return path
    return None


def _cleanup(scene_file: Path) -> None:
    """Remove temp scene file, ignoring errors."""
    try:
        if scene_file.exists():
            scene_file.unlink()
    except Exception as e:
        logger.warning(f"Failed to clean up {scene_file}: {e}")


def _log_directory_tree(directory: Path, max_depth: int = 4) -> None:
    """Log the directory tree for debugging."""
    if not directory.exists():
        logger.debug(f"Directory does not exist: {directory}")
        return
    for path in sorted(directory.rglob("*")):
        if len(path.relative_to(directory).parts) <= max_depth:
            logger.debug(f"  {path}")
