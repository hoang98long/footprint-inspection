"""Debug/research visualisation helpers, independent from core extraction."""

import numpy as np
from PIL import Image

DEFAULT_PREVIEW_MAX_DIMENSION = 1_600


def render_image_preview(image: Image.Image, max_dimension: int = DEFAULT_PREVIEW_MAX_DIMENSION) -> Image.Image:
    """Return an aspect-ratio-preserving display artifact without changing source data."""
    preview = image.copy()
    preview.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
    return preview


def render_point_cloud(points: np.ndarray, image_size: tuple[int, int], max_dimension: int = DEFAULT_PREVIEW_MAX_DIMENSION) -> Image.Image:
    """Render a display-only point-cloud preview efficiently, preserving aspect ratio.

    The source coordinates and the full point cloud are never resized or mutated.
    """
    width, height = image_size
    scale = min(1.0, max_dimension / max(width, height))
    preview_width, preview_height = max(1, round(width * scale)), max(1, round(height * scale))
    canvas = np.full((preview_height, preview_width), 255, dtype=np.uint8)
    if len(points):
        projected = np.floor(points.astype(float) * scale).astype(np.intp)
        valid = (projected[:, 0] >= 0) & (projected[:, 0] < preview_width) & (projected[:, 1] >= 0) & (projected[:, 1] < preview_height)
        canvas[projected[valid, 1], projected[valid, 0]] = 0
    return Image.fromarray(canvas, mode="L")
