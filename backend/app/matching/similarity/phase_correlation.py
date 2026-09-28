"""Full-original-image binary phase-correlation metrics (not an alignment method)."""

import numpy as np
from PIL import Image


def phase_correlation_metrics(q_image: Image.Image, k_image: Image.Image, threshold: int = 85) -> dict[str, float]:
    q = np.asarray(q_image.convert("L")) < threshold
    k = np.asarray(k_image.convert("L")) < threshold
    height, width = max(q.shape[0], k.shape[0]), max(q.shape[1], k.shape[1])
    q_canvas, k_canvas = np.zeros((height, width), dtype=float), np.zeros((height, width), dtype=float)
    q_canvas[: q.shape[0], : q.shape[1]] = q
    k_canvas[: k.shape[0], : k.shape[1]] = k
    cross_power = np.fft.fft2(q_canvas) * np.conj(np.fft.fft2(k_canvas))
    magnitude = np.abs(cross_power)
    correlation = np.fft.ifft2(cross_power / np.maximum(magnitude, np.finfo(float).eps)).real
    peak_index = np.unravel_index(np.argmax(correlation), correlation.shape)
    peak = float(correlation[peak_index])
    mean = float(np.mean(correlation))
    # PSR excludes a 5×5 neighbourhood around the peak; use a finite safe fallback.
    mask = np.ones(correlation.shape, dtype=bool)
    y, x = peak_index
    mask[max(0, y - 2): y + 3, max(0, x - 2): x + 3] = False
    sidelobes = correlation[mask]
    sidelobe_std = float(np.std(sidelobes))
    return {"peak_value": float(peak / mean) if abs(mean) > np.finfo(float).eps else 0.0, "psr": float((peak - np.mean(sidelobes)) / sidelobe_std) if sidelobe_std > np.finfo(float).eps else 0.0}
