"""Public response schemas for the shoeprint preprocessing endpoint."""

from pydantic import BaseModel, Field


class ImageMetadata(BaseModel):
    width: int
    height: int
    mode: str


class PreprocessingSettings(BaseModel):
    threshold: int = Field(ge=0, le=255)
    invert: bool
    edge_method: str
    coordinate_order: str = "xy"


class PointCloudStatistics(BaseModel):
    num_points: int
    min_x: int | None
    max_x: int | None
    min_y: int | None
    max_y: int | None
    width: int
    height: int
    density: float


class PreprocessingArtifacts(BaseModel):
    original: str
    grayscale: str
    edges: str
    processed: str
    point_cloud: str
    preview_points: list[list[int]]


class PreprocessingData(BaseModel):
    image: ImageMetadata
    preprocessing: PreprocessingSettings
    statistics: PointCloudStatistics
    artifacts: PreprocessingArtifacts
    processing_time_ms: float


class PreprocessingResponse(BaseModel):
    success: bool = True
    data: PreprocessingData
