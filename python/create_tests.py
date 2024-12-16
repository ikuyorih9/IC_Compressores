import os

def rotate_byte(filepath:str, rotate:int):
    """
    Rotate every byte from an input file by a selected value.

    Args:
        filepath (str): The path of the input file.
        rotate (int): The number of positions to rotate (positive for right, negative for left).
    """
    outpath = filepath + "_rotated_" + str(rotate) # Set the output path.
    with open(filepath, "rb") as entrada, open(outpath, "wb") as saida: # Open both input and output files
        while (byte := entrada.read(1)): # Get a byte from the input file.
            valor_incrementado = (byte[0] + rotate) % 256 # Rotate the byte.
            saida.write(bytes([valor_incrementado])) # Writes in the output file.

def rotate_some_bytes(filepath:str, rotate:int, bytelist: list) -> int:
    """
    Rotate selected bytes from an input file by a selected value.

    Args:
        filepath (str): The path of the input file.
        rotate (int): The number of positions to rotate (positive for right, negative for left).
        bytelist (list[int]): The indices of the bytes to rotate in the input file.

    Returns:
        int: The number of bytes changed.
    """

    outpath = filepath + "_rotated_" + str(rotate) + '_' + ''.join(map(str, bytelist)) # Set the output path.
    bytelist = [ord(c) for c in bytelist] # Refresh the str bytelist to its corresponding ASCII number

    cont = 0 # Initialize the counter for the number of bytes changed.

    with open(filepath, "rb") as entrada, open(outpath, "wb") as saida: # Open both input and output files
        while (byte := entrada.read(1)): # Get a byte from the input file.
            if byte[0] in bytelist: # If the byte read is in the bytelist, so...
                valor_incrementado = (byte[0] + rotate) % 256 # Rotate the byte.
                saida.write(bytes([valor_incrementado])) # Writes in the output file.
                cont += 1 # Increment the counter
            else: # If the byte read isn't in the bytelist, so...
                saida.write(byte) # Just copy the byte to the output file.

    return cont

def rotate_some_bytes_from_dir(dirpath:str, rotate:int, bytelist:list):
    """
    Rotate selected bytes in all files of a directory.

    Args:
        dirpath (str): the directory to get files.
        rotate (int): The number of positions to rotate (positive for right, negative for left).
        bytelist (list[int]): The indices of the bytes to rotate in the input file.
    """
    print(f"Rotating bytes {bytelist} from {dirpath} by {rotate}...")
    for filename in os.listdir(dirpath):
        full_path = os.path.join(dirpath, filename)
        if not os.path.isdir(full_path):
            bytes_rotated = rotate_some_bytes(full_path, rotate, bytelist)
            print(f"\t{filename}: {bytes_rotated} bytes rotated by {rotate}.")
    print("Done.")

def rotate_all_bytes_from_dir(dirpath:str, rotate: int):
    """
    Rotate selected bytes in all files of a directory.

    Args:
        dirpath (str): the directory to get files.
        rotate (int): The number of positions to rotate (positive for right, negative for left).
        bytelist (list[int]): The indices of the bytes to rotate in the input file.
    """
    print(f"Rotating all bytes from {dirpath} by {rotate}...")
    for filename in os.listdir(dirpath):
        full_path = os.path.join(dirpath, filename)
        if not os.path.isdir(full_path):
            rotate_byte(full_path, rotate)
            print(f"\t{filename}: all bytes rotated by {rotate}.")
    print("Done.")

def remove_redundant_data(dirpath: str, outpath: str):
    for filename in os.listdir(dirpath):
        full_path = os.path.join(dirpath, filename)
        if not os.path.isdir(full_path):
            print(f"Removing redundant data from file {filename}...")
            
            non_redundant_data = ""
            last_line = ""
            with open(full_path, 'r') as file:
                for line in file:
                    if last_line != line:
                        non_redundant_data += line
                        last_line = line
                    else: 
                        continue

            if not os.path.exists(outpath): # If the output path doesn't exist
                print(f"\tDirectory {outpath} doesn't exist. Creating...")
                os.makedirs(outpath, exist_ok=True) # Create the output path.
            
            output_path = os.path.join(outpath, filename)

            print(f"Writing non-redundant data in {output_path}")
            with open(output_path, 'w') as outfile:
                outfile.write(non_redundant_data)
