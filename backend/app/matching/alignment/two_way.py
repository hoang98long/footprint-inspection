"""Multi-start, two-way ICP search that always returns K transformed into Q space."""

from dataclasses import dataclass, asdict
from time import perf_counter
import numpy as np

from .config import ICPConfig
from .icp import run_icp
from .initialization import downsample_points, initial_translations
from .transforms import RigidTransform


@dataclass
class CandidateResult:
    direction: str
    initial_shift: str
    downsample_ratio: float
    transform: RigidTransform
    rmse: float
    iterations: int
    converged: bool
    correspondence_count: int
    processing_time_ms: float
    proportion_overlap: float = 0.0

    def public(self) -> dict[str, object]:
        return {**asdict(self), "transform": {"rotation_matrix": self.transform.rotation.tolist(), "translation": self.transform.translation.tolist(), "rotation_angle": self.transform.angle_degrees}}


def generate_candidates(q_points: np.ndarray, k_points: np.ndarray, config: ICPConfig) -> list[CandidateResult]:
    candidates: list[CandidateResult] = []
    for ratio_index, ratio in enumerate(config.downsample_ratios):
        q_sample = downsample_points(q_points, ratio, None if config.random_seed is None else config.random_seed + ratio_index * 2)
        k_sample = downsample_points(k_points, ratio, None if config.random_seed is None else config.random_seed + ratio_index * 2 + 1)
        for direction, source, target in (("k_to_q", k_sample, q_sample), ("q_to_k", q_sample, k_sample)):
            for shift_name, shift in initial_translations(source).items():
                started = perf_counter()
                try:
                    result = run_icp(source, target, shift, config)
                except ValueError:
                    continue
                # Direction B is inverted to preserve the public K → Q convention.
                transform = result.transform if direction == "k_to_q" else result.transform.inverse()
                candidates.append(CandidateResult(direction, shift_name, ratio, transform, result.rmse, result.iterations, result.converged, result.correspondence_count, (perf_counter() - started) * 1000))
    if not candidates:
        raise ValueError("ICP_FAILED: no valid alignment candidates were produced.")
    return candidates
