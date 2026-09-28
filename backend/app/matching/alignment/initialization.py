"""Deterministic initial shifts and non-mutating point-cloud downsampling."""

import numpy as np


def downsample_points(points: np.ndarray, ratio: float, random_seed: int | None) -> np.ndarray:
    if not 0 < ratio <= 1:
        raise ValueError("Downsample ratio must be in (0, 1].")
    if len(points) < 3:
        raise ValueError("At least three points are required for ICP.")
    count = max(3, int(round(len(points) * ratio)))
    count = min(count, len(points))
    if count == len(points):
        return points.copy()
    generator = np.random.default_rng(random_seed)
    return points[np.sort(generator.choice(len(points), size=count, replace=False))].copy()


def initial_translations(moving_points: np.ndarray) -> dict[str, np.ndarray]:
    """Paper's none/left/right/up/down shifts, based on moving-cloud ranges."""
    coordinate_range = moving_points.max(axis=0) - moving_points.min(axis=0)
    x_range, y_range = coordinate_range
    return {
        "none": np.array([0.0, 0.0]),
        "left": np.array([-2.0 * x_range, 0.0]),
        "right": np.array([2.0 * x_range, 0.0]),
        "up": np.array([0.0, -2.0 * y_range]),
        "down": np.array([0.0, 2.0 * y_range]),
    }
