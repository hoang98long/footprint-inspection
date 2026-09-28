"""Stable 35-feature vector used as Phase 3's future classifier input."""

from app.matching.alignment.transforms import RigidTransform
from .clustering import clustering_metrics
from .distance import minimum_distance_metrics
from .image_metrics import aligned_image_metrics
from .overlap import jaccard_indices, proportion_overlap
from .phase_correlation import phase_correlation_metrics

FEATURE_NAMES = ("q_points_count", "k_points_count", "q_overlap_1", "k_overlap_1", "q_overlap_2", "k_overlap_2", "q_overlap_3", "k_overlap_3", "q_overlap_5", "k_overlap_5", "q_overlap_10", "k_overlap_10", "jaccard_round_0", "jaccard_round_1", "jaccard_round_2", "mean_distance", "std_distance", "p10_distance", "p25_distance", "median_distance", "p75_distance", "p90_distance", "cdm_20", "cpm_20", "im_20", "twrm_20", "cdm_100", "cpm_100", "im_100", "twrm_100", "peak_value", "psr", "ncc", "mse", "ssim")
FEATURE_COUNT = len(FEATURE_NAMES)


def extract_similarity_features(q_points, k_aligned, q_image, k_image, transform: RigidTransform, random_state: int | None = 42) -> dict[str, float | int]:
    """Return JSON-safe, deterministic features in the fixed paper-derived order."""
    features: dict[str, float | int] = {"q_points_count": int(len(q_points)), "k_points_count": int(len(k_aligned))}
    features.update(proportion_overlap(q_points, k_aligned))
    features.update(jaccard_indices(q_points, k_aligned))
    features.update(minimum_distance_metrics(q_points, k_aligned))
    features.update(clustering_metrics(q_points, k_aligned, 20, random_state))
    features.update(clustering_metrics(q_points, k_aligned, 100, random_state))
    features.update(phase_correlation_metrics(q_image, k_image))
    features.update(aligned_image_metrics(q_image, k_image, transform))
    return {name: int(value) if isinstance(value, int) else float(value) for name, value in features.items() if name in FEATURE_NAMES}
