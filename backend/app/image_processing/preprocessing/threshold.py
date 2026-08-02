"""
Threshold module.

Supported:

- Otsu
- Binary
- Adaptive Mean
- Adaptive Gaussian
- Canny
"""

from __future__ import annotations

import cv2
import numpy as np


class ThresholdProcessor:

    @staticmethod
    def binary(
        gray: np.ndarray,
        threshold: int = 127,
    ) -> np.ndarray:

        _, img = cv2.threshold(
            gray,
            threshold,
            255,
            cv2.THRESH_BINARY,
        )

        return img

    @staticmethod
    def otsu(
        gray: np.ndarray,
    ) -> np.ndarray:

        _, img = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY + cv2.THRESH_OTSU,
        )

        return img

    @staticmethod
    def adaptive_mean(
        gray: np.ndarray,
        block_size: int = 31,
        c: int = 5,
    ) -> np.ndarray:

        return cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            block_size,
            c,
        )

    @staticmethod
    def adaptive_gaussian(
        gray: np.ndarray,
        block_size: int = 31,
        c: int = 5,
    ) -> np.ndarray:

        return cv2.adaptiveThreshold(
            gray,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            block_size,
            c,
        )

    @staticmethod
    def canny(
        gray: np.ndarray,
        low: int = 50,
        high: int = 150,
    ) -> np.ndarray:

        return cv2.Canny(
            gray,
            low,
            high,
        )

    @staticmethod
    def apply(
        gray: np.ndarray,
        method: str = "otsu",
    ) -> np.ndarray:

        method = method.lower()

        if method == "binary":
            return ThresholdProcessor.binary(gray)

        if method == "otsu":
            return ThresholdProcessor.otsu(gray)

        if method == "adaptive_mean":
            return ThresholdProcessor.adaptive_mean(gray)

        if method == "adaptive_gaussian":
            return ThresholdProcessor.adaptive_gaussian(gray)

        if method == "canny":
            return ThresholdProcessor.canny(gray)

        raise ValueError(f"Unknown threshold method: {method}")