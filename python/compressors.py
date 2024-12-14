import zlib
import gzip
import bz2

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

def zlib_compressed_size(data: bytes) -> int:
    compressor = zlib.compressobj(
        level=zlib.Z_BEST_COMPRESSION,  # Nível de compressão (0 a 9)
        method=zlib.DEFLATED,           # Método de compressão (DEFLATED é padrão)
        wbits=zlib.MAX_WBITS,           # Tamanho da janela (máximo é 15)
        memLevel=zlib.DEF_MEM_LEVEL,    # Uso de memória (1 a 9, padrão: 8)
        strategy=zlib.Z_FILTERED  # Estratégia de compressão
    )
    return len(compressor.compress(data)+ compressor.flush())

def zlib_ncd_original_data(x:bytes, y:bytes) -> float:
    """
    Calculates NCD from non compressed data X and Y. In this case, data are ZLIB compressed before calculate.

    Args:
        x (bytes): bytes from original file 1.
        y (bytes): bytes from original file 2.
    
    Returns:
        float: the NCD value.
    """
    cx = zlib_compressed_size(x)
    cy = zlib_compressed_size(y)
    
    xy = mix_data(x,y)
    cxy_mixed = zlib_compressed_size(xy)
    cxy_conc = zlib_compressed_size(x+y)

    if cxy_mixed <= cxy_conc:
        cxy = cxy_mixed
    else:
        cxy = cxy_conc

    print(f"cx = {cx}; cy = {cy}; cxy = {cxy}; min = {min(cx,cy)}; max = {max(cx,cy)} -> NCD={(cxy - min(cx, cy))/max(cx, cy)}")
    return (cxy - min(cx, cy))/max(cx, cy)

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


