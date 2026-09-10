"""Pillow-only image loading and edge operations used by the MVP baseline."""

from PIL import Image, ImageFilter, ImageOps


def load_grayscale_image(image: Image.Image) -> Image.Image:
    """Return a detached 8-bit grayscale image for RGB, RGBA, or L input."""
    if image.width <= 0 or image.height <= 0:
        raise ValueError("Image dimensions must be greater than zero.")
    return image.convert("L")


def detect_edges(image: Image.Image) -> Image.Image:
    """Detect deterministic Laplacian-style edges with Pillow FIND_EDGES."""
    return load_grayscale_image(image).filter(ImageFilter.FIND_EDGES)


def invert_image(image: Image.Image) -> Image.Image:
    """Invert an 8-bit grayscale image so detected edges become dark pixels."""
    return ImageOps.invert(load_grayscale_image(image))
