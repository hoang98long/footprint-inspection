"""Multipart API for Phase 2 alignment and feature-vector extraction."""

from io import BytesIO
import logging

from fastapi import APIRouter, File, Form, UploadFile, status
from fastapi.responses import JSONResponse
from PIL import Image, UnidentifiedImageError

from app.image_processing.preprocessing.config import PreprocessingConfig
from app.matching.alignment.config import ICPConfig
from app.schemas.matching import MatchingData, MatchingResponse
from app.services.matching_service import matching_service

router = APIRouter()
logger = logging.getLogger(__name__)
SUPPORTED_TYPES = {"image/jpeg", "image/png", "image/tiff"}


def _error(code: str, message: str) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"success": False, "error": {"code": code, "message": message}})


async def _load(upload: UploadFile) -> Image.Image | JSONResponse:
    if upload.content_type not in SUPPORTED_TYPES:
        return _error("INVALID_IMAGE", "Only PNG, JPG/JPEG, and TIFF images are supported.")
    try:
        image = Image.open(BytesIO(await upload.read()))
        image.load()
        return image
    except (UnidentifiedImageError, OSError):
        return _error("INVALID_IMAGE", "The uploaded file cannot be decoded as an image.")


async def _match(q_image: UploadFile, k_image: UploadFile, threshold: int, max_iterations: int, tolerance: float) -> MatchingResponse | JSONResponse:
    if not 0 <= threshold <= 255:
        return _error("INVALID_THRESHOLD", "Threshold must be between 0 and 255.")
    q, k = await _load(q_image), await _load(k_image)
    if isinstance(q, JSONResponse): return q
    if isinstance(k, JSONResponse): return k
    try:
        result = matching_service.match_shoeprints(q, k, PreprocessingConfig(threshold=threshold), ICPConfig(max_iterations=max_iterations, tolerance=tolerance))
    except ValueError as error:
        code = str(error).split(":", 1)[0] if ":" in str(error) else "ICP_FAILED"
        logger.info("Matching failed code=%s reason=%s", code, error)
        return _error(code, str(error))
    return MatchingResponse(data=MatchingData(**result))


@router.post("/matching/align", response_model=MatchingResponse)
async def align_shoeprints(q_image: UploadFile = File(...), k_image: UploadFile = File(...), threshold: int = Form(128), max_iterations: int = Form(100), tolerance: float = Form(1e-5)) -> MatchingResponse | JSONResponse:
    return await _match(q_image, k_image, threshold, max_iterations, tolerance)


@router.post("/matching/features", response_model=MatchingResponse)
async def match_features(q_image: UploadFile = File(...), k_image: UploadFile = File(...), threshold: int = Form(128), max_iterations: int = Form(100), tolerance: float = Form(1e-5)) -> MatchingResponse | JSONResponse:
    return await _match(q_image, k_image, threshold, max_iterations, tolerance)
