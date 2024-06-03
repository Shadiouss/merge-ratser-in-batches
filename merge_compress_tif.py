import os
import glob
from osgeo import gdal
import subprocess

def merge_tif_files_in_batches(input_dir, output_file, batch_size=100):
    """Merge all TIFF files in the specified directory into a single output file in batches.

    Args:
        input_dir (str): Path to the directory containing the TIFF files.
        output_file (str): Path to the output merged and compressed TIFF file.
        batch_size (int): Number of files to process in each batch.
    """
    print('Merging TIFF files in batches...')

    # Get list of all TIFF files in the directory
    input_files = glob.glob(os.path.join(input_dir, "*.tif"))

    if not input_files:
        raise FileNotFoundError("No TIFF files found in the specified directory.")

    total_files = len(input_files)
    print(f'Total number of files to merge: {total_files}')

    temp_files = []
    compress_options = [
        "-co", "COMPRESS=DEFLATE",
        "-co", "TILED=YES",
        "-co", "BIGTIFF=YES", 
        "-a_nodata", "0"
    ]
    
    for i in range(0, total_files, batch_size):
        batch_files = input_files[i:i + batch_size]
        batch_output_file = os.path.join(input_dir, f"batch_{i // batch_size}.tif")

        # Skip processing if the batch file already exists
        if os.path.exists(batch_output_file):
            print(f"Batch file {batch_output_file} already exists, skipping...")
            temp_files.append(batch_output_file)
            continue
        
        # Create a VRT file from batch TIFF files
        vrt_file = os.path.join(input_dir, f"batch_{i // batch_size}.vrt")
        vrt_options = gdal.BuildVRTOptions(resampleAlg='cubic')
        gdal.BuildVRT(vrt_file, batch_files, options=vrt_options)
        
        # Compress the VRT file to the final batch output file
        gdal.Translate(batch_output_file, vrt_file, options=gdal.TranslateOptions(options=compress_options))

        # Clean up the temporary VRT file
        os.remove(vrt_file)
        temp_files.append(batch_output_file)
        print(f"Processed batch {i // batch_size + 1}/{(total_files + batch_size - 1) // batch_size}")

    # Merge all batch files into the final output file
    vrt_file = os.path.join(input_dir, "final_merged.vrt")
    gdal.BuildVRT(vrt_file, temp_files, options=gdal.BuildVRTOptions(resampleAlg='cubic'))
    gdal.Translate(output_file, vrt_file, options=gdal.TranslateOptions(options=compress_options))

    # Clean up the temporary batch files and VRT file
    for temp_file in temp_files:
        os.remove(temp_file)
    os.remove(vrt_file)

    print(f"Merged and compressed TIFF file created at {output_file}")

def compress_tif(input_file, output_file):
    """Compress the TIFF file.

    Args:
        input_file (str): Path to the input TIFF file.
        output_file (str): Path to the output compressed TIFF file.
    """
    no_data_value = "0" 
    result = subprocess.run([
        "gdal_translate",
        "-co", "COMPRESS=JPEG",
        "-co", "PHOTOMETRIC=YCBCR",
        "-co", "JPEG_QUALITY=85",
        "-co", "TILED=YES",
        "-co", "BLOCKXSIZE=256",  
        "-co", "BLOCKYSIZE=256",  
        "-co", "BIGTIFF=YES",  
        "-a_nodata", no_data_value,  # Define no data value
        input_file,
        output_file
    ], capture_output=True, text=True)

    # Print the result
    print("Return code:", result.returncode)
    print("Standard output:", result.stdout)
    print("Standard error:", result.stderr)

# Usage example
if __name__ == "__main__":
    input_dir = "Path"
    output_file = "Path\\geotiff.tif"
    merge_tif_files_in_batches(input_dir, output_file)
    
    input_file = output_file
    compressed_output_file = "Path\\geotiff_compress.tif"
    compress_tif(input_file, compressed_output_file)
