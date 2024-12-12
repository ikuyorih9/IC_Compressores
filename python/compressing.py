import os
from compressors import *


def compress(data: bytes, compressor: str) -> bytes:
    """
    Compress data using a selected compressor.

    Args:
        data (bytes): data to compress.
        compressor (str): selected compressor
        
    Returns:
        bytes: compressed data.
    """
    if compressor == "zlib":
        return zlib_compress(data)
    
    elif compressor == "bz2":
        return bz2_compress(data)
    
    elif compressor == "gzip":
        return gzip_compress(data)
    else:
        "Selected compressor isn't available."


def ncd(x:bytes, y:bytes, compressor:str) -> float:
    """
    Calculate NCD value of two data using a selected compressor.

    Args:
        x (bytes): first data input to NCD.
        y (bytes): second data input to NCD.
        compressor (str): selected compressor

    Returns:
        float: NCD value from both data inputs.
    """
    if compressor == "zlib":
        return zlib_ncd(x, y)
    
    elif compressor == "bz2":
        return bz2_ncd(x, y)

    elif compressor == "gzip":
        return gzip_ncd(x, y)
    else:
        "Selected compressor isn't available."
        return -1.0

def compress_all_from_dir(dirpath:str, output_path:str, compressor:str):
    """
    Compress all files from a dir and writes all in output files.

    Args:
        dirpath (str): the directory to get files.
        output_path (str): the directory which output files will be saved.
        compressor (str): selected compressor.
    """
    output_path = os.path.join(output_path, compressor)
    print(f"Compressing all files from {dirpath} using {compressor}...")
    for filename in os.listdir(dirpath): # Get each filename from dir.
        full_path = os.path.join(dirpath, filename) # Get the full path of the file.
        if not os.path.isdir(full_path): # If the full path is not a directory, so...
            with open(full_path, 'rb') as file: # Open the file for binary read.
                print(f"\tOpening file {full_path} for binary read...")
                data = file.read() # Get data from the file.
                compressed = compress(data, compressor) # Compress data using selected compressor.

                     
            if not os.path.exists(output_path): # If the output path doesn't exist
                print(f"\tDirectory {output_path} doesn't exist. Creating...")
                os.makedirs(output_path, exist_ok=True) # Create the output path.
            
            output_file = os.path.join(output_path, filename) # Create output file path.
            with open(output_file, 'wb') as output: # Open the output file for binary write.
                print(f"\tWriting in {output_file}")
                output.write(compressed) # Writes compressed data in output.

    print("Done.")