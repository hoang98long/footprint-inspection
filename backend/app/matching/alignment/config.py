"""Configuration for deterministic multi-start, two-way 2D ICP."""

from dataclasses import dataclass

ICP_DOWNSAMPLE_RATIOS = (0.04, 0.05, 0.06, 0.20, 0.50)


@dataclass(frozen=True)
class ICPConfig:
    max_iterations: int = 100
    tolerance: float = 1e-5
    max_correspondence_distance: float = 1_000.0
    min_correspondences: int = 3
    random_seed: int | None = 42
    downsample_ratios: tuple[float, ...] = ICP_DOWNSAMPLE_RATIOS
    overlap_distance: float = 3.0

    def __post_init__(self) -> None:
        if self.max_iterations <= 0 or self.tolerance <= 0 or self.max_correspondence_distance <= 0:
            raise ValueError("ICP iteration, tolerance, and correspondence settings must be positive.")
        if self.min_correspondences < 3:
            raise ValueError("ICP requires at least three correspondences.")
        if not self.downsample_ratios or any(not 0 < ratio <= 1 for ratio in self.downsample_ratios):
            raise ValueError("Downsample ratios must be in (0, 1].")
