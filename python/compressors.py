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
    cxy = zlib_compressed_size(x+y, level, method, wbits, memLevel, strategy)

    # print(f"cx = {cx}; cy = {cy}; cxy = {cxy}; min = {min(cx,cy)}; max = {max(cx,cy)} -> NCD={(cxy - min(cx, cy))/max(cx, cy)}")
    return (cxy - min(cx, cy))/max(cx, cy)

def zlib_timed_ncd(x:bytes, y:bytes, level=zlib.Z_BEST_COMPRESSION, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS, memLevel=zlib.DEF_MEM_LEVEL, strategy=zlib.Z_DEFAULT_STRATEGY, rounds=1000, chunk_size=32<<10) -> tuple[float, float]:
    def timed_compress_len(data:bytes, level=zlib.Z_BEST_COMPRESSION, method=zlib.DEFLATED, wbits=zlib.MAX_WBITS, memLevel=zlib.DEF_MEM_LEVEL, strategy=zlib.Z_DEFAULT_STRATEGY) -> tuple[float,float]:
        zlib_compressor = zlib.compressobj(
            level=level,  # Nível de compressão (0 a 9)
            method=method,           # Método de compressão (DEFLATED é padrão)
            wbits=wbits,           # Tamanho da janela (máximo é 15)
            memLevel=memLevel,    # Uso de memória (1 a 9, padrão: 8)
            strategy=strategy  # Estratégia de compressão
        )
        start = process_time()
        compressed = zlib_compressor.compress(data) + zlib_compressor.flush()
        end = process_time()
        del zlib_compressor
        return len(compressed), (end-start)

    processing_time = 0
    for i in range(rounds):
        cx, tx = timed_compress_len(x, level, method, wbits, memLevel, strategy)
        cy, ty = timed_compress_len(y, level, method, wbits, memLevel, strategy)

        mix_start = process_time()
        xy = mix_bytes(x,y,chunk_size)
        mix_end = process_time()

        mix_time = mix_end - mix_start
        cxy, txy = timed_compress_len((xy), level, method, wbits, memLevel, strategy)
        processing_time += tx + ty + mix_time + txy

    processing_time /= rounds

    # print(f"cx = {cx}; cy = {cy}; cxy = {cxy}; min = {min(cx,cy)}; max = {max(cx,cy)} -> NCD={(cxy - min(cx, cy))/max(cx, cy)}")
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
    cxy = ppmd_compressed_size(x+y, order, mem_size, variant)

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
        del ppmd_compressor
        return len(compressed), (end-start)

    processing_time = 0
    for i in range(rounds):
        cx, tx = timed_compress_len(x, order, mem_size, variant)
        cy, ty = timed_compress_len(y, order, mem_size, variant)
        cxy, txy = timed_compress_len((x+y), order, mem_size, variant)
        processing_time += tx + ty + txy

    processing_time /= rounds

    return (cxy - min(cx, cy))/max(cx, cy), processing_time

def mix_bytes(x: bytes, y: bytes, chunk_size: int) -> bytes:
    """
    Intercala os bytes de dois streams em blocos de tamanho chunk_size.

    Parâmetros:
    - x: bytes do primeiro arquivo.
    - y: bytes do segundo arquivo.
    - chunk_size: tamanho do bloco de intercalação.

    Retorno:
    - Um único stream de bytes com os dados de x e y intercalados em blocos de chunk_size.
    """
    # Calcula os tamanhos dos streams
    len_x = len(x)
    len_y = len(y)

    # Calcula o tamanho total do resultado
    total_length = len_x + len_y

    # Cria um bytearray para o resultado (mais eficiente que concatenar bytes)
    result = bytearray(total_length)

    # Índices para percorrer os streams e o resultado
    i, j, k = 0, 0, 0

    # Intercala os blocos enquanto houver dados em x ou y
    while i < len_x or j < len_y:
        # Copia um bloco de x para o resultado, se ainda houver dados
        if i < len_x:
            end = min(i + chunk_size, len_x)
            result[k:k + (end - i)] = x[i:end]
            k += end - i
            i = end

        # Copia um bloco de y para o resultado, se ainda houver dados
        if j < len_y:
            end = min(j + chunk_size, len_y)
            result[k:k + (end - j)] = y[j:end]
            k += end - j
            j = end

    # Retorna o resultado como bytes
    return bytes(result)



