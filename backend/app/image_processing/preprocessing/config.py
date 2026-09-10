"""Configuration for the deterministic shoeprint preprocessing baseline."""

from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True)
class PreprocessingConfig:
    """Options for the paper-aligned grayscale/edge/point-cloud pipeline."""

    threshold: int = 128
    invert: bool = True
    edge_method: Literal["pillow_find_edges"] = "pillow_find_edges"
    coordinate_order: Literal["xy"] = "xy"
    max_points: int | None = None
    random_seed: int | None = 42

    def __post_init__(self) -> None:
        if not 0 <= self.threshold <= 255:
            raise ValueError("Threshold must be between 0 and 255.")
        if self.edge_method != "pillow_find_edges":
            raise ValueError("Only the 'pillow_find_edges' edge method is supported.")
        if self.coordinate_order != "xy":
            raise ValueError("Only the 'xy' coordinate order is supported.")
        if self.max_points is not None and self.max_points <= 0:
            raise ValueError("max_points must be greater than zero when provided.")
