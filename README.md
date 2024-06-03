# Raster Merge and Compress

This repository contains a Python script to merge and compress TIFF files in batches using GDAL.

## Usage

The script `merge_compress_tif.py` provides two main functions:
- `merge_tif_files_in_batches`: Merges all TIFF files in the specified directory into a single output file in batches.
- `compress_tif`: Compresses a TIFF file using JPEG compression.

## Prerequisites

- [GDAL](https://gdal.org/)
- Python packages: `osgeo`, `glob`

## Running the Script

Modify the `input_dir` and `output_file` variables in the script to point to your directory and desired output file. Then run the script:

```sh
python merge_compress_tif.py
