import zlib
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
    xy = mix_data(x,y)
    cxy_mixed = gzip_compressed_size(xy)
    cxy_conc = gzip_compressed_size(x+y)

    if cxy_mixed <= cxy_conc:
        cxy = cxy_mixed
    else:
        cxy = cxy_conc

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
    xy = mix_data(x,y)
    cxy_mixed = bz2_compressed_size(xy)
    cxy_conc = bz2_compressed_size(x+y)

    if cxy_mixed <= cxy_conc:
        cxy = cxy_mixed
    else:
        cxy = cxy_conc

    print(f"cx = {cx}; cy = {cy}; cxy = {cxy}; min = {min(cx,cy)}; max = {max(cx,cy)} -> NCD={(cxy - min(cx, cy))/max(cx, cy)}")
    return (cxy - min(cx, cy))/max(cx, cy)

# ZLIB COMPRESSING FUNCTIONS
def zlib_compress(data: bytes) -> bytes:
    return zlib.compress(data)

def zlib_compressed_size(data: bytes, level=zlib.Z_BEST_COMPRESSION, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS, memLevel=zlib.DEF_MEM_LEVEL, strategy=zlib.Z_FILTERED) -> int:
    compressor = zlib.compressobj(
        level=level,  # Nível de compressão (0 a 9)
        method=method,           # Método de compressão (DEFLATED é padrão)
        wbits=wbits,           # Tamanho da janela (máximo é 15)
        memLevel=memLevel,    # Uso de memória (1 a 9, padrão: 8)
        strategy=strategy  # Estratégia de compressão
    )
    return len(compressor.compress(data)+ compressor.flush())

def zlib_ncd_original_data(x:bytes, y:bytes, level=zlib.Z_BEST_COMPRESSION, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS, memLevel=zlib.DEF_MEM_LEVEL, strategy=zlib.Z_FILTERED) -> float:
    """
    Calculates NCD from non compressed data X and Y. In this case, data are ZLIB compressed before calculate.

    Args:
        x (bytes): bytes from original file 1.
        y (bytes): bytes from original file 2.
    
    Returns:
        float: the NCD value.
    """
    cx = zlib_compressed_size(x, level, method, wbits, memLevel, strategy)
    cy = zlib_compressed_size(y, level, method, wbits, memLevel, strategy)
    
    xy = mix_data(x,y)
    cxy_mixed = zlib_compressed_size(xy, level, method, wbits, memLevel, strategy)
    cxy_conc = zlib_compressed_size(x+y, level, method, wbits, memLevel, strategy)

    if cxy_mixed <= cxy_conc:
        cxy = cxy_mixed
    else:
        cxy = cxy_conc

    cxy = cxy_conc

    # print(f"cx = {cx}; cy = {cy}; cxy = {cxy}; min = {min(cx,cy)}; max = {max(cx,cy)} -> NCD={(cxy - min(cx, cy))/max(cx, cy)}")
    return (cxy - min(cx, cy))/max(cx, cy)

def zlib_timed_ncd(x:bytes, y:bytes, level=zlib.Z_BEST_COMPRESSION, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS, memLevel=zlib.DEF_MEM_LEVEL, strategy=zlib.Z_FILTERED, rounds=1000) -> tuple[float, float]:
    def timed_compress_len(data:bytes, level=zlib.Z_BEST_COMPRESSION, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS, memLevel=zlib.DEF_MEM_LEVEL, strategy=zlib.Z_FILTERED) -> tuple[float,float]:
        zlib_compressor = zlib.compressobj(
            level=level,  # Nível de compressão (0 a 9)
            method=method,           # Método de compressão (DEFLATED é padrão)
            wbits=wbits,           # Tamanho da janela (máximo é 15)
            memLevel=memLevel,    # Uso de memória (1 a 9, padrão: 8)
            strategy=strategy  # Estratégia de compressão
        )
        start = process_time()
        compressed = zlib_compressor.compress(data)
        end = process_time()
        return len(compressed), (end-start)

    processing_time = 0
    for i in range(rounds):
        cx, tx = timed_compress_len(x, level, method, wbits, memLevel, strategy)
        cy, ty = timed_compress_len(y, level, method, wbits, memLevel, strategy)
        cxy, txy = timed_compress_len((x+y), level, method, wbits, memLevel, strategy)
        processing_time += tx + ty + txy

    processing_time /= rounds

    print(f"cx = {cx}; cy = {cy}; cxy = {cxy}; min = {min(cx,cy)}; max = {max(cx,cy)} -> NCD={(cxy - min(cx, cy))/max(cx, cy)}")
    return (cxy - min(cx, cy))/max(cx, cy), processing_time

# PPMd COMPRESSING FUNCTIONS
def ppmd_compress(data: bytes) -> bytes:
    return pyppmd.compress(data)

def ppmd_compressed_size(data: bytes, order=6, mem_size = 16<<20, variant="I") -> int:
    compressor = pyppmd.PpmdCompressor(
        max_order=order,
        mem_size=mem_size,
        variant=variant
    )
    return len(compressor.compress(data))

def ppmd_ncd_original_data(x:bytes, y:bytes, order=6, mem_size = 16<<20, variant="I") -> float:
    """
    Calculates NCD from non compressed data X and Y. In this case, data are ZLIB compressed before calculate.

    Args:
        x (bytes): bytes from original file 1.
        y (bytes): bytes from original file 2.
    
    Returns:
        float: the NCD value.
    """
    cx = ppmd_compressed_size(x, order, mem_size, variant)
    cy = ppmd_compressed_size(y, order, mem_size, variant)
    
    xy = mix_data(x,y)
    cxy_mixed = ppmd_compressed_size(xy, order, mem_size, variant)
    cxy_conc = ppmd_compressed_size(x+y, order, mem_size, variant)

    if cxy_mixed <= cxy_conc:
        cxy = cxy_mixed
    else:
        cxy = cxy_conc

    # print(f"cx = {cx}; cy = {cy}; cxy = {cxy}; min = {min(cx,cy)}; max = {max(cx,cy)} -> NCD={(cxy - min(cx, cy))/max(cx, cy)}")
    return (cxy - min(cx, cy))/max(cx, cy)

def ppmd_timed_ncd(x:bytes, y:bytes, order=6, mem_size = 16<<20, variant="I", rounds=1000) -> tuple[float, float]:
    def timed_compress_len(data:bytes, order=6, mem_size = 16<<20, variant="I") -> tuple[float,float]:
        ppmd_compressor = pyppmd.PpmdCompressor(
            max_order=order,
            mem_size=mem_size,
            variant=variant
        )
        start = process_time()
        compressed = ppmd_compressor.compress(data)
        end = process_time()
        return len(compressed), (end-start)

    processing_time = 0
    for i in range(rounds):
        cx, tx = timed_compress_len(x, order, mem_size, variant)
        cy, ty = timed_compress_len(y, order, mem_size, variant)
        cxy, txy = timed_compress_len((x+y), order, mem_size, variant)
        processing_time += tx + ty + txy

    processing_time /= rounds

    return (cxy - min(cx, cy))/max(cx, cy), processing_time

def mix_data(x: bytes, y: bytes) -> bytes:
    """
    Intercala os bytes de x e y. Se x e y tiverem tamanhos diferentes,
    os bytes restantes da entrada maior serão adicionados ao final.

    Args:
        x (bytes): Primeira sequência de bytes.
        y (bytes): Segunda sequência de bytes.

    Returns:
        bytes: Sequência de bytes intercalada.
    """
    # Intercalar até o menor comprimento
    mixed = b''.join(bytes([a]) + bytes([b]) for a, b in zip(x, y))
    
    # Adicionar os bytes restantes, se houver
    if len(x) > len(y):
        mixed += x[len(y):]
    elif len(y) > len(x):
        mixed += y[len(x):]
    
    return mixed


