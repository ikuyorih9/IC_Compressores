import os
import csv
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
    
    elif compressor == "ppmd":
        return ppmd_compress(data)
    else:
        "Selected compressor isn't available."

def ncd(x:bytes, y:bytes, compressor:str) -> float:
    """
    Calculate NCD value of two non compressed data using a selected compressor.

    Args:
        x (bytes): first data input to NCD.
        y (bytes): second data input to NCD.
        compressor (str): selected compressor

    Returns:
        float: NCD value from both data inputs.
    """
    if compressor == "zlib":
        return zlib_ncd_original_data(x, y)
    
    elif compressor == "bz2":
        return bz2_ncd_original_data(x, y)

    elif compressor == "gzip":
        return gzip_ncd_original_data(x, y)
    
    elif compressor == "ppmd":
        return ppmd_ncd_original_data(x, y)
    
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
    # print(f"Compressing all files from {dirpath} using {compressor}...")
    for filename in os.listdir(dirpath): # Get each filename from dir.
        full_path = os.path.join(dirpath, filename) # Get the full path of the file.
        if not os.path.isdir(full_path): # If the full path is not a directory, so...
            with open(full_path, 'rb') as file: # Open the file for binary read.
                # print(f"\tOpening file {full_path} for binary read...")
                data = file.read() # Get data from the file.
                compressed = compress(data, compressor) # Compress data using selected compressor.

                     
            if not os.path.exists(output_path): # If the output path doesn't exist
                # print(f"\tDirectory {output_path} doesn't exist. Creating...")
                os.makedirs(output_path, exist_ok=True) # Create the output path.
            
            output_file = os.path.join(output_path, filename) # Create output file path.
            with open(output_file, 'wb') as output: # Open the output file for binary write.
                # print(f"\tWriting in {output_file}")
                output.write(compressed) # Writes compressed data in output.

    # print("Done.")

def open_files_from_dir(dir:str, n:int) -> list:
    """
    Open files from a directory and save them in a list.

    Args:
        dir (str): the path of the directory.
        n (int): number of files to be open.
    Returns:
        list: data list of the opened files.
    """
    try:
        datalist = []
        cont = 0

        for filename in os.listdir(dir): # Open every filename from the directory.
            if cont == n:
                break
            rpath = os.path.join(dir, filename) # Get the path of the file.

            # print(f"\tOpening file {rpath}...")

            with open(rpath, 'rb') as file: # Open the file.
                data = file.read() # Read the file.
                datalist.append((data, filename)) # Append to the return list.

            cont += 1
        return datalist # Return the data list.
    except FileNotFoundError as fnfe:
        print(f"ERROR: {fnfe}")
        return None

def create_ncd_mixed_matrix(dir1_path:str, dir1_qtt:int, dir2_path:str, dir2_qtt:int, output_path:str, compressor:str):
    """
    Create the NCD matrix with mixed files from different directories. Then the NCD matrix and the NCD sorted list are saved in the output directory.

    Args:
        dir1_path (str): the first directory to open.
        dir1_qtt (int): quantity of files to be open from directory 1.
        dir2_path (str): the second directory to open.
        dir2_qtt (int): quantity of files to be open from directory 2.
        output_path (str): the output directory to store the results.
        compressor (str): the selected compressor.
    """

    try:
        # print(f"Opening {dir1_qtt} files from {dir1_path}...")
        data = open_files_from_dir(dir1_path, dir1_qtt) # Open the first set of compressed files
        
        # print(f"Opening {dir2_qtt} files from {dir2_path}..")
        data.extend(open_files_from_dir(dir2_path, dir2_qtt)) # Append the second set of compressed files to the datalist.
    except Exception as e:
        print("ERROR: an error happened while opening files from directories")
        return
    
    n = len(data) # Get the datalist size.

    ncd_matrix = [[0.0] * (n + 1) for _ in range(n + 1)]
    for i in range (n):
        ncd_matrix[i+1][0] = data[i][1]

    ordered_data = []

    for i in range(n):
        for j in range(n):
            ncd_value = ncd(data[i][0], data[j][0], compressor)
            ncd_matrix[i+1][j+1] = ncd_value
            ordered_data.append((data[i][1], data[j][1], ncd_value))

    output_path = os.path.join(output_path, compressor)

    if not os.path.exists(output_path): # If the output path doesn't exist
        # print(f"\tDirectory {output_path} doesn't exist. Creating...")
        os.makedirs(output_path, exist_ok=True) # Create the output path.

    # print("Writing the NCD matrix...")

    results_filename = os.path.join(output_path, "ncd_matrix.tsv")
    with open(results_filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow([""] + [data[i][1] for i in range(n)])
        
        for i in range(n):
            linha_formatada = [data[i][1]] + [f"{num:.5f}".replace(".", ",") for num in ncd_matrix[i + 1][1:]]
            writer.writerow(linha_formatada)

    # print(f"Writing sorted NCD values...")
    
    sorted_data = sorted(ordered_data, key=lambda x: x[2])

    sorted_path = os.path.join(output_path, "sorted_ncd.csv")
    with open(sorted_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter="\t")
        # Escrevendo as linhas da matriz no arquivo
        for item in sorted_data:
            linha_formatada = [item[0], item[1], f"{item[2]:.5f}".replace(".", ",")]
            writer.writerow(linha_formatada)

def create_ncd_matrix(dir_path:str, output_path:str, compressor:str):
    """
    Create the NCD matrix with mixed files from different directories. Then the NCD matrix and the NCD sorted list are saved in the output directory.

    Args:
        dir1_path (str): the first directory to open.
        dir1_qtt (int): quantity of files to be open from directory 1.
        dir2_path (str): the second directory to open.
        dir2_qtt (int): quantity of files to be open from directory 2.
        output_path (str): the output directory to store the results.
        compressor (str): the selected compressor.
    """

    try:
        # print(f"Opening all files from {dir_path}...")
        data = open_files_from_dir(dir_path, -1) # Open the first set of compressed files

    except Exception as e:
        print("ERROR: an error happened while opening files from directories")
        return
    
    n = len(data) # Get the datalist size.

    ncd_matrix = [[0.0] * (n + 1) for _ in range(n + 1)]
    for i in range (n):
        ncd_matrix[i+1][0] = data[i][1]

    ordered_data = []

    for i in range(n):
        for j in range(n):
            ncd_value = ncd(data[i][0], data[j][0], compressor)
            ncd_matrix[i+1][j+1] = ncd_value
            ordered_data.append((data[i][1], data[j][1], ncd_value))

    output_path = os.path.join(output_path, compressor)

    if not os.path.exists(output_path): # If the output path doesn't exist
        # print(f"\tDirectory {output_path} doesn't exist. Creating...")
        os.makedirs(output_path, exist_ok=True) # Create the output path.

    # print("Writing the NCD matrix...")

    results_filename = os.path.join(output_path, "ncd_matrix.tsv")
    with open(results_filename, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter="\t")
        writer.writerow([""] + [data[i][1] for i in range(n)])
        
        for i in range(n):
            linha_formatada = [data[i][1]] + [f"{num:.5f}".replace(".", ",") for num in ncd_matrix[i + 1][1:]]
            writer.writerow(linha_formatada)

    # print(f"Writing sorted NCD values...")
    
    sorted_data = sorted(ordered_data, key=lambda x: x[2])

    sorted_path = os.path.join(output_path, "sorted_ncd.csv")
    with open(sorted_path, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter="\t")
        # Escrevendo as linhas da matriz no arquivo
        for item in sorted_data:
            linha_formatada = [item[0], item[1], f"{item[2]:.5f}".replace(".", ",")]
            writer.writerow(linha_formatada)