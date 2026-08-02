"""
Perspective correction module.

Functions:
- Detect largest contour
- Approximate 4 corners
- Warp perspective
"""

from __future__ import annotations

import cv2
import numpy as np


class PerspectiveCorrection:

    @staticmethod
    def order_points(points: np.ndarray) -> np.ndarray:
        """
        Order points:
            top-left
            top-right
            bottom-right
            bottom-left
        """

        rect = np.zeros((4, 2), dtype=np.float32)

        s = points.sum(axis=1)

        rect[0] = points[np.argmin(s)]
        rect[2] = points[np.argmax(s)]

        diff = np.diff(points, axis=1)

        rect[1] = points[np.argmin(diff)]
        rect[3] = points[np.argmax(diff)]

        return rect

    @staticmethod
    def warp(image: np.ndarray) -> np.ndarray:

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        edge = cv2.Canny(blur, 50, 150)

        contours, _ = cv2.findContours(
            edge,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        if len(contours) == 0:
            return image

        contour = max(contours, key=cv2.contourArea)

        peri = cv2.arcLength(contour, True)

        approx = cv2.approxPolyDP(
            contour,
            0.02 * peri,
            True,
        )

        if len(approx) != 4:
            return image

        pts = approx.reshape(4, 2)

        rect = PerspectiveCorrection.order_points(pts)

        tl, tr, br, bl = rect

        widthA = np.linalg.norm(br - bl)
        widthB = np.linalg.norm(tr - tl)

        maxWidth = int(max(widthA, widthB))

        heightA = np.linalg.norm(tr - br)
        heightB = np.linalg.norm(tl - bl)

        maxHeight = int(max(heightA, heightB))

        dst = np.array(
            [
                [0, 0],
                [maxWidth - 1, 0],
                [maxWidth - 1, maxHeight - 1],
                [0, maxHeight - 1],
            ],
            dtype=np.float32,
        )

        matrix = cv2.getPerspectiveTransform(rect, dst)

        warped = cv2.warpPerspective(
            image,
            matrix,
            (maxWidth, maxHeight),
        )

        return warped