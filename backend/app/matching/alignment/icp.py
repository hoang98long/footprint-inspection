"""KD-tree based standard iterative closest point implementation."""

from dataclasses import dataclass
import numpy as np
from scipy.spatial import cKDTree

from .config import ICPConfig
from .transforms import IDENTITY_TRANSFORM, RigidTransform, estimate_rigid_transform


@dataclass
class ICPResult:
    transform: RigidTransform
    rmse: float
    iterations: int
    converged: bool
    correspondence_count: int


def run_icp(source_points: np.ndarray, target_points: np.ndarray, initial_translation: np.ndarray, config: ICPConfig) -> ICPResult:
    """Fit a rigid source→target transform using nearest neighbours from ``cKDTree``."""
    if len(source_points) < config.min_correspondences or len(target_points) < config.min_correspondences:
        raise ValueError("INSUFFICIENT_POINTS: not enough points for ICP.")
    tree = cKDTree(target_points)
    transform = RigidTransform(IDENTITY_TRANSFORM.rotation, np.asarray(initial_translation, dtype=float))
    prior_error = np.inf
    correspondence_count = 0
    for iteration in range(1, config.max_iterations + 1):
        transformed = transform.apply(source_points)
        distances, indexes = tree.query(transformed, k=1, distance_upper_bound=config.max_correspondence_distance)
        valid = np.isfinite(distances) & (indexes < len(target_points))
        correspondence_count = int(valid.sum())
        if correspondence_count < config.min_correspondences:
            raise ValueError("ICP_FAILED: insufficient in-range correspondences.")
        update = estimate_rigid_transform(transformed[valid], target_points[indexes[valid]])
        transform = update.compose(transform)
        error = float(np.sqrt(np.mean(distances[valid] ** 2)))
        if abs(prior_error - error) < config.tolerance:
            return ICPResult(transform, error, iteration, True, correspondence_count)
        prior_error = error
    return ICPResult(transform, float(prior_error), config.max_iterations, False, correspondence_count)
