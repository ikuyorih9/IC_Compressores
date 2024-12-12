import zlib
import gzip
import bz2

# GZIP COMPRESSING FUNCTIONS
def gzip_compress(data:bytes) -> bytes:
    return gzip.compress(data)

def gzip_compressed_size(data: bytes) -> int:
    return len(gzip.compress(data))

def gzip_ncd(x:bytes, y:bytes) -> float:
    cx = gzip_compressed_size(x)
    cy = gzip_compressed_size(y)
    cxy = gzip_compressed_size(x+y)
    return (cxy - min(cx, cy))/max(cx, cy)

# BZ2 COMPRESSING FUNCTIONS
def bz2_compress(data: bytes) -> bytes:
    return bz2.compress(data)

def bz2_compressed_size(data:bytes) -> int:
    return len(bz2.compress(data))

def bz2_ncd(x:bytes, y:bytes) -> float:
    cx = bz2_compressed_size(x)
    cy = bz2_compressed_size(y)
    cxy = bz2_compressed_size(x+y)
    return (cxy - min(cx, cy))/max(cx, cy)

# ZLIB COMPRESSING FUNCTIONS
def zlib_compress(data: bytes) -> bytes:
    return zlib.compress(data)

def zlib_compressed_size(data: bytes) -> int:
    return len(zlib.compress(data))

def zlib_ncd(x:bytes, y:bytes) -> float:
    cx = zlib_compressed_size(x)
    cy = zlib_compressed_size(y)
    cxy = zlib_compressed_size(x+y)
    return (cxy - min(cx, cy))/max(cx, cy)
