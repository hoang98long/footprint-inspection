"""Synchronous MVP endpoint for the paper-aligned shoeprint preprocessing flow."""

import base64
from io import BytesIO
import logging

import numpy as np
from fastapi import APIRouter, File, Form, UploadFile, status
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError

from app.image_processing.preprocessing.config import PreprocessingConfig
from app.image_processing.preprocessing.pipeline import preprocess_shoeprint
from app.image_processing.preprocessing.visualization import render_point_cloud
from app.schemas.preprocessing import (
    ImageMetadata,
    PointCloudStatistics,
    PreprocessingArtifacts,
    PreprocessingData,
    PreprocessingResponse,
    PreprocessingSettings,
)

router = APIRouter()
logger = logging.getLogger(__name__)
SUPPORTED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/tiff"}
SUPPORTED_SUFFIXES = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
MAX_UPLOAD_BYTES = 25 * 1024 * 1024
PREVIEW_POINT_LIMIT = 5_000


def _bad_request(code: str, message: str) -> JSONResponse:
    """Keep validation failures in the public API response convention."""
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"success": False, "error": {"code": code, "message": message}})


def _as_data_url(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def _preview_points(points: np.ndarray) -> list[list[int]]:
    if len(points) <= PREVIEW_POINT_LIMIT:
        sample = points
    else:
        indexes = np.linspace(0, len(points) - 1, PREVIEW_POINT_LIMIT, dtype=int)
        sample = points[indexes]
    return sample.tolist()


@router.post("/preprocess", response_model=PreprocessingResponse)
async def preprocess_image(
    image: UploadFile = File(...),
    threshold: int = Form(128),
    invert: bool = Form(True),
) -> PreprocessingResponse | JSONResponse:
    """Create an immutable full point cloud plus display-safe preview artifacts."""
    suffix = (image.filename or "").lower().rsplit(".", 1)
    extension = f".{suffix[-1]}" if len(suffix) == 2 else ""
    if image.content_type not in SUPPORTED_CONTENT_TYPES or extension not in SUPPORTED_SUFFIXES:
        return _bad_request("INVALID_IMAGE", "Only PNG, JPG/JPEG, and TIFF images are supported.")
    if not 0 <= threshold <= 255:
        return _bad_request("INVALID_THRESHOLD", "Threshold must be between 0 and 255.")
    content = await image.read()
    if not content or len(content) > MAX_UPLOAD_BYTES:
        return _bad_request("INVALID_IMAGE", "Image is empty or exceeds the 25 MB upload limit.")
    try:
        source = Image.open(BytesIO(content))
        source.load()
        if source.width <= 0 or source.height <= 0:
            raise ValueError("empty dimensions")
    except (UnidentifiedImageError, OSError, ValueError) as error:
        logger.info("Rejected invalid image filename=%s reason=%s", image.filename, error)
        return _bad_request("INVALID_IMAGE", "The uploaded file cannot be decoded as a valid image.")

    result = preprocess_shoeprint(source, PreprocessingConfig(threshold=threshold, invert=invert))
    if result.statistics["num_points"] == 0:
        return _bad_request("EMPTY_POINT_CLOUD", "No point cloud points were extracted for this threshold.")

    point_cloud_image = render_point_cloud(result.point_cloud, result.grayscale.size)
    logger.info("Preprocessed image filename=%s dimensions=%sx%s threshold=%s invert=%s points=%s duration_ms=%.2f", image.filename, source.width, source.height, threshold, invert, len(result.point_cloud), result.processing_time_ms)
    return PreprocessingResponse(data=PreprocessingData(
        image=ImageMetadata(**result.image_metadata),
        preprocessing=PreprocessingSettings(threshold=threshold, invert=invert, edge_method="pillow_find_edges"),
        statistics=PointCloudStatistics(**result.statistics),
        artifacts=PreprocessingArtifacts(
            original=_as_data_url(result.original),
            grayscale=_as_data_url(result.grayscale),
            edges=_as_data_url(result.edges),
            processed=_as_data_url(result.processed),
            point_cloud=_as_data_url(point_cloud_image),
            preview_points=_preview_points(result.point_cloud),
        ),
        processing_time_ms=round(result.processing_time_ms, 2),
    ))
