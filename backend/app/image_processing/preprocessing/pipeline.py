"""Paper-aligned baseline preprocessing: grayscale → edges → invert → point cloud."""

from time import perf_counter

from PIL import Image

from .config import PreprocessingConfig
from .edge_detection import detect_edges, invert_image, load_grayscale_image
from .models import PreprocessingResult
from .point_cloud import extract_point_cloud, point_cloud_statistics


def preprocess_shoeprint(image: Image.Image, config: PreprocessingConfig | None = None) -> PreprocessingResult:
    """Run the deterministic pipeline without geometric transformations or enhancement."""
    config = config or PreprocessingConfig()
    started = perf_counter()
    original = image.copy()
    grayscale = load_grayscale_image(image)
    edges = detect_edges(grayscale)
    processed = invert_image(edges) if config.invert else edges.copy()
    points = extract_point_cloud(processed, config.threshold)
    statistics = point_cloud_statistics(points, grayscale.size)
    return PreprocessingResult(
        original=original,
        grayscale=grayscale,
        edges=edges,
        processed=processed,
        point_cloud=points,
        statistics=statistics,
        config=config,
        processing_time_ms=(perf_counter() - started) * 1000,
    )
