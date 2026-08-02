
from pathlib import Path
import cv2
import numpy as np

class ImageLoader:
    """Load and save images."""

    @staticmethod
    def load(path:str|Path, color:bool=True)->np.ndarray:
        flag=cv2.IMREAD_COLOR if color else cv2.IMREAD_GRAYSCALE
        img=cv2.imread(str(path), flag)
        if img is None:
            raise FileNotFoundError(path)
        return img

    @staticmethod
    def save(path:str|Path, image:np.ndarray)->None:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(path), image)

    @staticmethod
    def info(image:np.ndarray)->dict:
        return {
            "shape": image.shape,
            "dtype": str(image.dtype),
            "channels": 1 if image.ndim==2 else image.shape[2]
        }
