"""In-memory result contract for shoeprint preprocessing."""

from dataclasses import dataclass

import numpy as np
from PIL import Image

from .config import PreprocessingConfig


@dataclass
class PreprocessingResult:
    original: Image.Image
    grayscale: Image.Image
    edges: Image.Image
    processed: Image.Image
    point_cloud: np.ndarray
    statistics: dict[str, int | float | None]
    config: PreprocessingConfig
    processing_time_ms: float

    @property
    def image_metadata(self) -> dict[str, int | str]:
        return {"width": self.original.width, "height": self.original.height, "mode": "L"}
