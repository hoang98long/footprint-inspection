"""Debug/research visualisation helpers, independent from core extraction."""

import numpy as np
from PIL import Image, ImageDraw


def render_point_cloud(points: np.ndarray, image_size: tuple[int, int]) -> Image.Image:
    """Render points at their original coordinates on a white canvas."""
    canvas = Image.new("L", image_size, color=255)
    if len(points):
        ImageDraw.Draw(canvas).point([tuple(point) for point in points.tolist()], fill=0)
    return canvas
