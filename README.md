# Synthetic Binary Lines Dataset for Hough Transform Benchmark

Dataset of **72 deterministic synthetic binary images** for comparing CPU and GPU implementations of the line Hough transform.

## Images
- Six resolutions: 256×256, 512×512, 1024×1024, 1920×1080 (FHD), 2560×1440 (QHD), 3840×2160 (4K).
- Four requested numbers of line segments: 10, 50, 100, 500.
- Three different randomized realizations per resolution/count combination.
- 8-bit grayscale PNG, black background (0), white lines (255), 1 pixel width.
- Each line segment connects two pseudorandomly selected perimeter points. Lines may overlap, cross or occasionally lie on a border. The count is the number of drawing operations, not the number of visually distinct lines.

## Metadata
`metadata.csv` lists image dimensions, requested line count, replicate, deterministic RNG seed, actual number and fraction of white pixels, and SHA-256 checksum.

## Reproduction
Install Python 3 and Pillow (`python -m pip install pillow`) and run `python generate_dataset.py` from this folder. The script uses deterministic seeds; file contents are expected to match when using a compatible Pillow version.

## Benchmark guidance
Use identical images and Hough parameters on CPU and GPU. The actual **white pixel count**, not just line count or resolution, affects workload. Measure separately GPU kernel time and end-to-end time including data transfers, synchronize the GPU before stopping the timer, and exclude warm-up/JIT runs. Report CPU sequential vs parallel mode and ensure equivalent accumulator results.

**Limitations:** Synthetic idealized lines are not representative of real photographs. This dataset is designed for controlled runtime benchmarking, not for estimating detection accuracy in natural scenes. With perimeter-based generation, actual edge density varies with resolution and line count, and not every line is guaranteed to span the entire image.
