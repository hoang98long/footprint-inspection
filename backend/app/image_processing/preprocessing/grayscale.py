
import cv2
import numpy as np

class GrayConverter:
    @staticmethod
    def to_gray(image:np.ndarray)->np.ndarray:
        if image.ndim==2:
            return image
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    @staticmethod
    def to_rgb(gray:np.ndarray)->np.ndarray:
        return cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
