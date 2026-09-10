"""Unit tests for the Pillow FIND_EDGES preprocessing baseline."""

import numpy as np
import pytest
from PIL import Image

from app.image_processing.preprocessing.config import PreprocessingConfig
from app.image_processing.preprocessing.edge_detection import detect_edges, invert_image, load_grayscale_image
from app.image_processing.preprocessing.pipeline import preprocess_shoeprint
from app.image_processing.preprocessing.point_cloud import extract_point_cloud, point_cloud_statistics


def test_load_image_and_grayscale_conversion() -> None:
    image = Image.new("RGBA", (3, 2), (40, 80, 120, 128))
    grayscale = load_grayscale_image(image)
    assert grayscale.mode == "L"
    assert grayscale.size == (3, 2)


def test_edge_detection_is_deterministic() -> None:
    image = Image.new("L", (4, 4), 255)
    image.putpixel((1, 1), 0)
    assert np.array_equal(np.asarray(detect_edges(image)), np.asarray(detect_edges(image)))


def test_invert() -> None:
    assert invert_image(Image.new("L", (1, 1), 25)).getpixel((0, 0)) == 230


def test_extract_point_cloud_uses_xy_coordinates() -> None:
    image = Image.new("L", (3, 3), 255)
    image.putpixel((1, 1), 10)
    assert extract_point_cloud(image, 128).tolist() == [[1, 1]]


def test_threshold_validation() -> None:
    with pytest.raises(ValueError, match="between 0 and 255"):
        PreprocessingConfig(threshold=256)


def test_preprocess_pipeline_is_deterministic() -> None:
    image = Image.new("RGB", (8, 8), "white")
    first = preprocess_shoeprint(image, PreprocessingConfig(threshold=128))
    second = preprocess_shoeprint(image, PreprocessingConfig(threshold=128))
    assert np.array_equal(first.point_cloud, second.point_cloud)
    assert first.grayscale.mode == first.edges.mode == first.processed.mode == "L"


def test_empty_point_cloud_statistics() -> None:
    points = extract_point_cloud(Image.new("L", (2, 2), 255), 0)
    assert points.shape == (0, 2)
    assert point_cloud_statistics(points, (2, 2))["num_points"] == 0
