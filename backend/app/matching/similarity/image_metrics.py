"""Image similarity in Q's unresized coordinate frame after applying K→Q rigid transform."""

import numpy as np
from PIL import Image
from skimage.metrics import structural_similarity

from app.matching.alignment.transforms import RigidTransform


def warp_k_to_q_frame(k_image: Image.Image, q_image: Image.Image, transform: RigidTransform) -> np.ndarray:
    inverse = transform.inverse()
    # Pillow affine coefficients map output(Q) coordinates to input(K) coordinates.
    matrix = inverse.rotation
    offset = inverse.translation
    data = (matrix[0, 0], matrix[0, 1], offset[0], matrix[1, 0], matrix[1, 1], offset[1])
    return np.asarray(k_image.convert("L").transform(q_image.size, Image.Transform.AFFINE, data, resample=Image.Resampling.BILINEAR, fillcolor=255), dtype=float)


def aligned_image_metrics(q_image: Image.Image, k_image: Image.Image, transform: RigidTransform) -> dict[str, float]:
    q = np.asarray(q_image.convert("L"), dtype=float)
    k = warp_k_to_q_frame(k_image, q_image, transform)
    q_binary, k_binary = (q < 85).astype(float), (k < 85).astype(float)
    q_centered, k_centered = q_binary - q_binary.mean(), k_binary - k_binary.mean()
    denominator = float(np.sqrt(np.sum(q_centered ** 2) * np.sum(k_centered ** 2)))
    ncc = float(np.sum(q_centered * k_centered) / denominator) if denominator > np.finfo(float).eps else 0.0
    mse = float(np.mean((q_binary - k_binary) ** 2))
    minimum = min(q_binary.shape)
    window = min(7, minimum if minimum % 2 else minimum - 1)
    ssim = float(structural_similarity(q_binary, k_binary, data_range=1.0, win_size=window)) if window >= 3 else 0.0
    return {"ncc": ncc, "mse": mse, "ssim": ssim}
