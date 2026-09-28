"""High-level Phase 2 orchestration: preprocessing, alignment, then feature extraction."""

from dataclasses import dataclass
from time import perf_counter
import base64
from io import BytesIO
import logging

import numpy as np
from PIL import Image, ImageDraw

from app.image_processing.preprocessing.config import PreprocessingConfig
from app.image_processing.preprocessing.pipeline import preprocess_shoeprint
from app.matching.alignment.config import ICPConfig
from app.matching.alignment.two_way import CandidateResult, generate_candidates
from app.matching.similarity.features import extract_similarity_features
from app.matching.similarity.overlap import proportion_overlap

logger = logging.getLogger(__name__)


@dataclass
class AlignmentResult:
    q_points: np.ndarray
    k_aligned: np.ndarray
    selected: CandidateResult
    candidate_results: list[CandidateResult]
    processing_time_ms: float

    def public(self) -> dict[str, object]:
        return {"rotation_matrix": self.selected.transform.rotation.tolist(), "rotation_angle": self.selected.transform.angle_degrees, "translation": self.selected.transform.translation.tolist(), "selected_downsample_ratio": self.selected.downsample_ratio, "selected_initial_shift": self.selected.initial_shift, "selected_direction": self.selected.direction, "rmse": self.selected.rmse, "iterations": self.selected.iterations, "converged": self.selected.converged, "correspondence_count": self.selected.correspondence_count, "proportion_overlap": self.selected.proportion_overlap, "candidate_results": [candidate.public() for candidate in self.candidate_results], "processing_time_ms": self.processing_time_ms}


def _data_url(image: Image.Image) -> str:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffer.getvalue()).decode("ascii")


def _overlay(q_points: np.ndarray, k_points: np.ndarray, size: tuple[int, int]) -> Image.Image:
    image = Image.new("RGB", size, "white")
    drawing = ImageDraw.Draw(image)
    for x, y in q_points:
        if 0 <= x < size[0] and 0 <= y < size[1]: drawing.point((int(x), int(y)), fill=(20, 100, 220))
    for x, y in k_points:
        if 0 <= x < size[0] and 0 <= y < size[1]: drawing.point((int(x), int(y)), fill=(220, 60, 70))
    return image


class MatchingService:
    def match_shoeprints(self, q_image: Image.Image, k_image: Image.Image, preprocessing_config: PreprocessingConfig | None = None, icp_config: ICPConfig | None = None) -> dict[str, object]:
        """Return Q/K* in Q coordinates plus 35 Phase 2 similarity features."""
        started = perf_counter()
        preprocessing_config, icp_config = preprocessing_config or PreprocessingConfig(), icp_config or ICPConfig()
        q_result, k_result = preprocess_shoeprint(q_image, preprocessing_config), preprocess_shoeprint(k_image, preprocessing_config)
        if len(q_result.point_cloud) < icp_config.min_correspondences or len(k_result.point_cloud) < icp_config.min_correspondences:
            raise ValueError("INVALID_POINT_CLOUD: each image must produce at least three points.")
        icp_started = perf_counter()
        candidates = generate_candidates(q_result.point_cloud, k_result.point_cloud, icp_config)
        for candidate in candidates:
            overlap = proportion_overlap(q_result.point_cloud, candidate.transform.apply(k_result.point_cloud))
            candidate.proportion_overlap = overlap["q_overlap_3"]
        selected = max(candidates, key=lambda candidate: (candidate.proportion_overlap, -candidate.rmse))
        k_aligned = selected.transform.apply(k_result.point_cloud)
        alignment = AlignmentResult(q_result.point_cloud, k_aligned, selected, candidates, (perf_counter() - icp_started) * 1000)
        similarity_started = perf_counter()
        features = extract_similarity_features(q_result.point_cloud, k_aligned, q_result.original, k_result.original, selected.transform, icp_config.random_seed)
        similarity_time = (perf_counter() - similarity_started) * 1000
        logger.info("Matched shoeprints candidates=%s selected_overlap=%.4f icp_ms=%.2f similarity_ms=%.2f total_ms=%.2f", len(candidates), selected.proportion_overlap, alignment.processing_time_ms, similarity_time, (perf_counter() - started) * 1000)
        return {"alignment": alignment.public(), "similarity": features, "artifacts": {"q_original": _data_url(q_result.original), "k_original": _data_url(k_result.original), "alignment_overlay": _data_url(_overlay(q_result.point_cloud, k_aligned, q_result.grayscale.size))}, "timing": {"total_icp_time_ms": alignment.processing_time_ms, "similarity_time_ms": similarity_time, "total_matching_time_ms": (perf_counter() - started) * 1000}}


matching_service = MatchingService()
