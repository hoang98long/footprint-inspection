"""KD-tree point-cloud overlap and rounded-coordinate Jaccard metrics."""

import numpy as np
from scipy.spatial import cKDTree

OVERLAP_DISTANCES = (1, 2, 3, 5, 10)


def _proportion(source: np.ndarray, target: np.ndarray, distance: float) -> float:
    if not len(source) or not len(target):
        return 0.0
    nearest, _ = cKDTree(target).query(source, k=1)
    return float(np.mean(nearest <= distance))


def proportion_overlap(q_points: np.ndarray, k_points: np.ndarray) -> dict[str, float]:
    result: dict[str, float] = {}
    for distance in OVERLAP_DISTANCES:
        result[f"q_overlap_{distance}"] = _proportion(q_points, k_points, distance)
        result[f"k_overlap_{distance}"] = _proportion(k_points, q_points, distance)
    return result


def jaccard_indices(q_points: np.ndarray, k_points: np.ndarray) -> dict[str, float]:
    output: dict[str, float] = {}
    for decimals in (0, 1, 2):
        q_set = {tuple(row) for row in np.round(q_points, decimals).tolist()}
        k_set = {tuple(row) for row in np.round(k_points, decimals).tolist()}
        union = q_set | k_set
        output[f"jaccard_round_{decimals}"] = float(len(q_set & k_set) / len(union)) if union else 0.0
    return output
