"""
Contrast enhancement module.

Supported methods:
- CLAHE
- Histogram Equalization
- Gamma Correction
"""

from __future__ import annotations

import cv2
import numpy as np


class ContrastEnhancer:

    @staticmethod
    def clahe(
        image: np.ndarray,
        clip_limit: float = 2.0,
        tile_grid_size: tuple[int, int] = (8, 8),
    ) -> np.ndarray:
        """
        Apply CLAHE.

        Parameters
        ----------
        clip_limit : float
        tile_grid_size : tuple
        """

        if image.ndim == 2:
            clahe = cv2.createCLAHE(
                clipLimit=clip_limit,
                tileGridSize=tile_grid_size,
            )
            return clahe.apply(image)

        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)

        l, a, b = cv2.split(lab)

        clahe = cv2.createCLAHE(
            clipLimit=clip_limit,
            tileGridSize=tile_grid_size,
        )

        l = clahe.apply(l)

        merged = cv2.merge((l, a, b))

        return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)

    @staticmethod
    def histogram_equalization(
        image: np.ndarray,
    ) -> np.ndarray:

        if image.ndim == 2:
            return cv2.equalizeHist(image)

        ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)

        y, cr, cb = cv2.split(ycrcb)

        y = cv2.equalizeHist(y)

        merged = cv2.merge((y, cr, cb))

        return cv2.cvtColor(merged, cv2.COLOR_YCrCb2BGR)

    @staticmethod
    def gamma(
        image: np.ndarray,
        gamma: float = 1.2,
    ) -> np.ndarray:

        inv_gamma = 1.0 / gamma

        table = np.array(
            [
                ((i / 255.0) ** inv_gamma) * 255
                for i in np.arange(256)
            ]
        ).astype("uint8")

        return cv2.LUT(image, table)

    @staticmethod
    def apply(
        image: np.ndarray,
        method: str = "clahe",
    ) -> np.ndarray:

        method = method.lower()

        if method == "clahe":
            return ContrastEnhancer.clahe(image)

        if method == "hist":
            return ContrastEnhancer.histogram_equalization(image)

        if method == "gamma":
            return ContrastEnhancer.gamma(image)

        raise ValueError(f"Unknown contrast method: {method}")