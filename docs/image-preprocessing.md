# Image preprocessing

## Purpose

This MVP provides the reproducible preprocessing baseline used before future shoeprint alignment. It deliberately produces a raw `numpy.ndarray` point cloud and has no dependency on matching or ICP modules.

```mermaid
flowchart LR
    A[Input Shoeprint] --> B[Grayscale]
    B --> C[Edge Detection]
    C --> D[Invert]
    D --> E[Darkness Threshold]
    E --> F[2D Point Cloud]
    F --> G[Future ICP Alignment]
```

## Algorithm

Pillow converts RGB/RGBA/L input to grayscale (`L`). `ImageFilter.FIND_EDGES` detects deterministic Laplacian-style edges. The edge image is inverted by default so edges are dark; every pixel with intensity strictly below `threshold` becomes one `[x, y]` point. No resize, normalisation, denoising, contrast enhancement, morphology, contour extraction, or geometric transformation is applied.

Coordinates use `xy`: `x` is the image column and `y` is the image row. The full point cloud is preserved as `PreprocessingResult.point_cloud` with shape `(N, 2)`, ready for future `Q_points`/`K_points` ICP inputs. Display previews may be sampled independently and never replace this data.

## Configuration

`PreprocessingConfig` defaults to `threshold=128`, `invert=True`, `edge_method="pillow_find_edges"`, and `coordinate_order="xy"`. Threshold values must be in 0–255; the edge method and coordinate order are intentionally fixed in this baseline.

## API and frontend

`POST /api/v1/preprocess` accepts multipart fields `image`, optional `threshold`, and optional `invert`. PNG, JPG/JPEG, and supported TIFF images are accepted up to 25 MB. The response contains base64 PNG artifacts for this MVP, statistics, and a bounded `preview_points` array. Invalid images, invalid thresholds, and empty point clouds return HTTP 400 with a structured error detail.

The **Tiền xử lý ảnh** menu opens the upload, parameter, visualization, statistics, reset, and threshold-comparison UI. Try the listed thresholds to support manual tuning; the application does not select a “best” threshold.

## Limitations and next step

Artifacts are returned inline for MVP convenience, so very large images increase response size. No ICP, matching, similarity metric, feature extraction, or model inference is implemented. A future alignment module should consume the unchanged `np.ndarray[N, 2]` output directly.
