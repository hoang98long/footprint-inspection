"""
Run:

python backend/tests/test_preprocessing.py \
    --input backend/assets/input/test.jpg
"""

from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]

sys.path.append(str(ROOT))

from app.image_processing.preprocessing.pipeline import (
    PreprocessingPipeline,
)


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Input image",
    )

    parser.add_argument(
        "--output",
        default="backend/assets/output",
    )

    args = parser.parse_args()

    pipeline = PreprocessingPipeline(
        contrast_method="clahe",
        denoise_method="bilateral",
        threshold_method="otsu",
        rotate_angle=10,
    )

    results = pipeline.process(args.input)

    pipeline.save_results(
        results,
        args.output,
    )

    print("\nProcessing finished.\n")

    for key in results:
        print(f"✓ {key}")


if __name__ == "__main__":
    main()