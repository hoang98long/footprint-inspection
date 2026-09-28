"""Ward-initialised deterministic K-means metrics from the referenced methodology."""

import logging
import numpy as np
from scipy.cluster.hierarchy import cut_tree, linkage
from sklearn.cluster import KMeans

logger = logging.getLogger(__name__)


def _within_variation(points: np.ndarray, labels: np.ndarray, centers: np.ndarray) -> float:
    terms = []
    for index in range(len(centers)):
        cluster = points[labels == index]
        if len(cluster):
            terms.append(float(np.mean(np.sum((cluster - centers[index]) ** 2, axis=1))))
    return float(np.mean(terms)) if terms else 0.0


def clustering_metrics(q_points: np.ndarray, k_points: np.ndarray, cluster_count: int, random_state: int | None) -> dict[str, float]:
    prefix = str(cluster_count)
    empty = {f"cdm_{prefix}": 0.0, f"cpm_{prefix}": 0.0, f"im_{prefix}": 0.0, f"twrm_{prefix}": 0.0}
    effective_count = min(cluster_count, len(q_points), len(k_points))
    if effective_count < 2:
        logger.warning("Skipping clustering k=%s because clouds have insufficient points.", cluster_count)
        return empty
    if effective_count != cluster_count:
        logger.warning("Reducing clustering k=%s to k=%s because of point-cloud size.", cluster_count, effective_count)
    labels = cut_tree(linkage(q_points, method="ward"), n_clusters=[effective_count]).ravel()
    centers = np.vstack([q_points[labels == index].mean(axis=0) for index in range(effective_count)])
    q_kmeans = KMeans(n_clusters=effective_count, init=centers, n_init=1, random_state=random_state).fit(q_points)
    k_kmeans = KMeans(n_clusters=effective_count, init=q_kmeans.cluster_centers_, n_init=1, random_state=random_state).fit(k_points)
    # Correspondence is inherited from Q-centroid initialisation; it is not re-sorted.
    cdm = float(np.sqrt(np.mean(np.sum((q_kmeans.cluster_centers_ - k_kmeans.cluster_centers_) ** 2, axis=1))))
    q_proportions = np.bincount(q_kmeans.labels_, minlength=effective_count) / len(q_points)
    k_proportions = np.bincount(k_kmeans.labels_, minlength=effective_count) / len(k_points)
    cpm = float(np.sqrt(np.mean((q_proportions - k_proportions) ** 2)))
    q_tw = _within_variation(q_points, q_kmeans.labels_, q_kmeans.cluster_centers_)
    k_tw = _within_variation(k_points, k_kmeans.labels_, k_kmeans.cluster_centers_)
    twrm = float((q_tw - k_tw) / q_tw) if q_tw > np.finfo(float).eps else 0.0
    return {f"cdm_{prefix}": cdm, f"cpm_{prefix}": cpm, f"im_{prefix}": float(k_kmeans.n_iter_), f"twrm_{prefix}": twrm}
