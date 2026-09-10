"""Point-cloud extraction utilities. Coordinates always follow the (x, y) convention."""

import numpy as np
from PIL import Image


def extract_point_cloud(processed_image: Image.Image, threshold: int) -> np.ndarray:
    """Extract [x, y] rows for every pixel whose intensity is below ``threshold``."""
    if not 0 <= threshold <= 255:
        raise ValueError("Threshold must be between 0 and 255.")
    pixels = np.asarray(processed_image.convert("L"), dtype=np.uint8)
    y_coordinates, x_coordinates = np.where(pixels < threshold)
    return np.column_stack((x_coordinates, y_coordinates)).astype(np.int32, copy=False)


def point_cloud_statistics(points: np.ndarray, image_size: tuple[int, int] | None = None) -> dict[str, int | float | None]:
    """Return bounds and density without mutating or normalising the source points."""
    if points.size == 0:
        return {"num_points": 0, "min_x": None, "max_x": None, "min_y": None, "max_y": None, "width": 0, "height": 0, "density": 0.0}
    min_x, min_y = points.min(axis=0).tolist()
    max_x, max_y = points.max(axis=0).tolist()
    density = float(len(points) / (image_size[0] * image_size[1])) if image_size else 0.0
    return {"num_points": int(len(points)), "min_x": int(min_x), "max_x": int(max_x), "min_y": int(min_y), "max_y": int(max_y), "width": int(max_x - min_x), "height": int(max_y - min_y), "density": density}
