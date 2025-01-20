from zlib_compressing import *
import gzip
import bz2
import pyppmd
from time import process_time

# GZIP COMPRESSING FUNCTIONS
def gzip_compress(data:bytes) -> bytes:
    return gzip.compress(data)

def gzip_compressed_size(data: bytes) -> int:
    return len(gzip.compress(data))

def gzip_ncd_original_data(x:bytes, y:bytes) -> float:
    """
    Calculates NCD from non compressed data X and Y. In this case, data are GZIP compressed before calculate.

    Args:
        x (bytes): bytes from original file 1.
        y (bytes): bytes from original file 2.
    
    Returns:
        float: the NCD value.
    """
    cx = gzip_compressed_size(x)
    cy = gzip_compressed_size(y)
    cxy = gzip_compressed_size(x+y)

    print(f"cx = {cx}; cy = {cy}; cxy = {cxy}; min = {min(cx,cy)}; max = {max(cx,cy)} -> NCD={(cxy - min(cx, cy))/max(cx, cy)}")
    return (cxy - min(cx, cy))/max(cx, cy)

# BZ2 COMPRESSING FUNCTIONS
def bz2_compress(data: bytes) -> bytes:
    return bz2.compress(data)

def bz2_compressed_size(data:bytes) -> int:
    return len(bz2.compress(data))

def bz2_ncd_original_data(x:bytes, y:bytes) -> float:
    """
    Calculates NCD from non compressed data X and Y. In this case, data are BZ2 compressed before calculate.

    Args:
        x (bytes): bytes from original file 1.
        y (bytes): bytes from original file 2.
    
    Returns:
        float: the NCD value.
    """
    cx = bz2_compressed_size(x)
    cy = bz2_compressed_size(y)
    cxy = bz2_compressed_size(x+y)

    print(f"cx = {cx}; cy = {cy}; cxy = {cxy}; min = {min(cx,cy)}; max = {max(cx,cy)} -> NCD={(cxy - min(cx, cy))/max(cx, cy)}")
    return (cxy - min(cx, cy))/max(cx, cy)



