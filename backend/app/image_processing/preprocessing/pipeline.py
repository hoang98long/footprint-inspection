"""
Preprocessing Pipeline

Current pipeline:

Load
    ↓
Gray
    ↓
CLAHE
    ↓
Denoise
    ↓
Threshold
    ↓
Perspective
    ↓
Rotation
"""

from pathlib import Path

import cv2
import numpy as np

from .image_loader import ImageLoader
from .grayscale import GrayConverter
from .contrast import ContrastEnhancer
from .denoise import Denoiser
from .threshold import ThresholdProcessor
from .perspective import PerspectiveCorrection
from .rotation import RotationCorrection


class PreprocessingPipeline:

    def __init__(
        self,
        contrast_method: str = "clahe",
        denoise_method: str = "bilateral",
        threshold_method: str = "otsu",
        rotate_angle: float = 0,
    ):
        self.contrast_method = contrast_method
        self.denoise_method = denoise_method
        self.threshold_method = threshold_method
        self.rotate_angle = rotate_angle

    def process(self, image_path: str | Path) -> dict[str, np.ndarray]:

        image = ImageLoader.load(image_path)

        results = {}

        results["original"] = image

        gray = GrayConverter.to_gray(image)
        results["gray"] = gray

        contrast = ContrastEnhancer.apply(
            gray,
            method=self.contrast_method,
        )
        results["contrast"] = contrast

        denoise = Denoiser.apply(
            contrast,
            method=self.denoise_method,
        )
        results["denoise"] = denoise

        threshold = ThresholdProcessor.apply(
            denoise,
            method=self.threshold_method,
        )
        results["threshold"] = threshold

        # Perspective và Rotation yêu cầu ảnh màu
        perspective = PerspectiveCorrection.warp(image)
        results["perspective"] = perspective

        rotation = RotationCorrection.rotate_angle(perspective, angle=self.rotate_angle)
        results["rotation"] = rotation

        return results

    @staticmethod
    def save_results(
        results: dict[str, np.ndarray],
        output_dir: str | Path,
    ):

        output_dir = Path(output_dir)

        output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        order = [
            "original",
            "gray",
            "contrast",
            "denoise",
            "threshold",
            "perspective",
            "rotation",
        ]

        for idx, key in enumerate(order):

            filename = output_dir / f"{idx:02d}_{key}.png"

            cv2.imwrite(str(filename), results[key])

        print(f"Saved to: {output_dir}")