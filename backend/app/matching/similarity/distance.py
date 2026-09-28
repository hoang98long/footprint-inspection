"""Minimum-distance distribution from Q points to aligned K points."""

import numpy as np
from scipy.spatial import cKDTree


def minimum_distance_metrics(q_points: np.ndarray, k_points: np.ndarray) -> dict[str, float]:
    if not len(q_points) or not len(k_points):
        return {key: 0.0 for key in ("mean_distance", "std_distance", "p10_distance", "p25_distance", "median_distance", "p75_distance", "p90_distance")}
    distances, _ = cKDTree(k_points).query(q_points, k=1)
    return {"mean_distance": float(np.mean(distances)), "std_distance": float(np.std(distances)), "p10_distance": float(np.percentile(distances, 10)), "p25_distance": float(np.percentile(distances, 25)), "median_distance": float(np.percentile(distances, 50)), "p75_distance": float(np.percentile(distances, 75)), "p90_distance": float(np.percentile(distances, 90))}
