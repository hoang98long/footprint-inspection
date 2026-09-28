"""Synthetic regression tests for Phase 2 rigid ICP and similarity features."""

import numpy as np
from PIL import Image

from app.matching.alignment.config import ICPConfig, ICP_DOWNSAMPLE_RATIOS
from app.matching.alignment.icp import run_icp
from app.matching.alignment.initialization import downsample_points, initial_translations
from app.matching.alignment.transforms import RigidTransform, make_rotation
from app.matching.alignment.two_way import generate_candidates
from app.matching.similarity.clustering import clustering_metrics
from app.matching.similarity.distance import minimum_distance_metrics
from app.matching.similarity.features import FEATURE_COUNT, FEATURE_NAMES, extract_similarity_features
from app.matching.similarity.image_metrics import aligned_image_metrics
from app.matching.similarity.overlap import jaccard_indices, proportion_overlap


def cloud() -> np.ndarray:
    grid_x, grid_y = np.meshgrid(np.arange(20), np.arange(20))
    return np.column_stack((grid_x.ravel(), grid_y.ravel())).astype(float)


def test_icp_recovers_translation_and_rotation() -> None:
    q = np.random.default_rng(7).uniform(-10, 10, size=(400, 2))
    known = RigidTransform(make_rotation(np.radians(10)), np.array([20.0, 30.0]))
    k = known.inverse().apply(q)
    result = run_icp(k, q, np.array([20.0, 30.0]), ICPConfig(max_iterations=200, max_correspondence_distance=100))
    assert result.converged
    assert result.rmse < 0.2
    assert np.allclose(result.transform.translation, known.translation, atol=1.0)


def test_initialisation_and_downsampling_are_complete_and_deterministic() -> None:
    assert set(initial_translations(cloud())) == {"none", "left", "right", "up", "down"}
    assert np.array_equal(downsample_points(cloud(), .2, 42), downsample_points(cloud(), .2, 42))
    assert ICP_DOWNSAMPLE_RATIOS == (0.04, 0.05, 0.06, 0.20, 0.50)


def test_two_way_search_evaluates_both_directions() -> None:
    points = cloud()
    candidates = generate_candidates(points, points + [2, 3], ICPConfig(max_iterations=20, max_correspondence_distance=100))
    assert {candidate.direction for candidate in candidates} == {"k_to_q", "q_to_k"}
    assert {candidate.initial_shift for candidate in candidates} == {"none", "left", "right", "up", "down"}


def test_overlap_jaccard_and_distance_metrics() -> None:
    points = np.array([[0., 0.], [1., 1.]])
    assert proportion_overlap(points, points)["q_overlap_1"] == 1.0
    assert jaccard_indices(points, points)["jaccard_round_2"] == 1.0
    assert minimum_distance_metrics(points, points)["mean_distance"] == 0.0


def test_clustering_and_image_metrics_are_finite() -> None:
    points = cloud()
    metrics = clustering_metrics(points, points + .1, 20, 42)
    assert set(metrics) == {"cdm_20", "cpm_20", "im_20", "twrm_20"}
    image = Image.new("L", (20, 20), 255)
    image.putpixel((5, 5), 0)
    assert aligned_image_metrics(image, image, RigidTransform(np.eye(2), np.zeros(2)))["ssim"] == 1.0


def test_feature_contract_has_exactly_35_json_safe_features() -> None:
    points = cloud()
    image = Image.new("L", (20, 20), 255)
    features = extract_similarity_features(points, points, image, image, RigidTransform(np.eye(2), np.zeros(2)))
    assert FEATURE_COUNT == len(FEATURE_NAMES) == len(features) == 35
    assert all(np.isfinite(value) for value in features.values())
