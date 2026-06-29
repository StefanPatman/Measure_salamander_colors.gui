from pathlib import Path
from time import perf_counter

from .types import MeasureResults


def initialize():
    import itaxotools

    itaxotools.progress_handler("Initializing...")
    from itaxotools.salamander_colors import measure  # noqa


def execute(
    input_path: Path,
    output_path: Path,
    extension: str,
    background_threshold: int,
    black_threshold: int,
) -> MeasureResults:
    from itaxotools import progress_handler
    from itaxotools.salamander_colors.measure import measure_color

    ts = perf_counter()

    header = "Sample\tBackground_pixels\tTotal_pixels\tBlack_pixels\tBlack_percent\tYellow_pixels\tYellow_percent\tRatio\tOther_pixels\n"
    lines = [header]

    images = sorted(input_path.rglob(f"*{extension}"))
    total = len(images)

    for i, image_path in enumerate(images):
        progress_handler(f"Processing {image_path.name}", i, 0, total)
        row = measure_color(image_path, background_threshold, black_threshold)
        lines.append(image_path.stem + "\t" + "\t".join(str(v) for v in row) + "\n")

    progress_handler("Writing results...", total, 0, total)
    output_path.write_text("".join(lines))

    tf = perf_counter()
    return MeasureResults(output_path, tf - ts)
