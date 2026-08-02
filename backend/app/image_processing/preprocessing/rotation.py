"""
Rotation normalization.

Automatically rotate the shoeprint so
its long axis is vertical.
"""

from __future__ import annotations

import cv2
import numpy as np


class RotationCorrection:

    @staticmethod
    def rotate(
        image: np.ndarray,
    ) -> np.ndarray:

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(
            gray,
            0,
            255,
            cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU,
        )

        coords = np.column_stack(
            np.where(binary > 0)
        )

        if len(coords) < 10:
            return image

        rect = cv2.minAreaRect(coords)

        angle = rect[-1]

        if angle < -45:
            angle = 90 + angle

        angle = -angle

        h, w = image.shape[:2]

        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(
            center,
            angle,
            1.0,
        )

        rotated = cv2.warpAffine(
            image,
            matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )

        return rotated

    @staticmethod
    def rotate_angle(
        image: np.ndarray,
        angle: float,
    ) -> np.ndarray:

        h, w = image.shape[:2]

        center = (w // 2, h // 2)

        matrix = cv2.getRotationMatrix2D(
            center,
            angle,
            1,
        )

        return cv2.warpAffine(
            image,
            matrix,
            (w, h),
            flags=cv2.INTER_CUBIC,
        )