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

def zlib_and_ppmd_timed_ncd(
        x:bytes, 
        y:bytes, 
        zlib_params = [zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, zlib.Z_DEFAULT_STRATEGY],
        ppmd_params = [12, 512<<10, "I"], 
        zlib_first = True,
        rounds=1
) -> tuple[float, float]:
    def zlib_ppmd_timed_compress_len(
            data:bytes, 
            zlib_params = [zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, zlib.Z_DEFAULT_STRATEGY],
            ppmd_params = [12, 512<<10, "I"]) -> tuple[float,float]:
        
        zlib_compressor = zlib.compressobj(
            level=zlib_params[0],  # Nível de compressão (0 a 9)
            method=zlib_params[1],           # Método de compressão (DEFLATED é padrão)
            wbits=zlib_params[2],           # Tamanho da janela (máximo é 15)
            memLevel=zlib_params[3],    # Uso de memória (1 a 9, padrão: 8)
            strategy=zlib_params[4]  # Estratégia de compressão
        )
        start = process_time()
        zlib_compressed = zlib_compressor.compress(data) + zlib_compressor.flush()
        end = process_time()
        del zlib_compressor

        t1 = end - start

        ppmd_compressor = pyppmd.PpmdCompressor(
            max_order=ppmd_params[0],
            mem_size=ppmd_params[1],
            variant=ppmd_params[2]
        )
        start = process_time()
        ppmd_compressed = ppmd_compressor.compress(zlib_compressed) + ppmd_compressor.flush()
        end = process_time()

        t2 = end - start

        del ppmd_compressor
        return len(ppmd_compressed), (t1+t2)
    
    def ppmd_zlib_timed_compress_len(
            data:bytes, 
            zlib_params = [zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, zlib.Z_DEFAULT_STRATEGY],
            ppmd_params = [12, 512<<10, "I"]) -> tuple[float,float]:

        ppmd_compressor = pyppmd.PpmdCompressor(
            max_order=ppmd_params[0],
            mem_size=ppmd_params[1],
            variant=ppmd_params[2]
        )
        start = process_time()
        ppmd_compressed = ppmd_compressor.compress(data) + ppmd_compressor.flush()
        end = process_time()
        del ppmd_compressor

        t1 = end - start

        zlib_compressor = zlib.compressobj(
            level=zlib_params[0],  # Nível de compressão (0 a 9)
            method=zlib_params[1],           # Método de compressão (DEFLATED é padrão)
            wbits=zlib_params[2],           # Tamanho da janela (máximo é 15)
            memLevel=zlib_params[3],    # Uso de memória (1 a 9, padrão: 8)
            strategy=zlib_params[4]  # Estratégia de compressão
        )
        start = process_time()
        zlib_compressed = zlib_compressor.compress(ppmd_compressed) + zlib_compressor.flush()
        end = process_time()
        del zlib_compressor

        t2 = end - start

        return len(zlib_compressed), (t1+t2)

    processing_time = 0
    if zlib_first:
        for i in range(rounds):
            cx, tx = zlib_ppmd_timed_compress_len(x, zlib_params=zlib_params, ppmd_params=ppmd_params)
            cy, ty = zlib_ppmd_timed_compress_len(y, zlib_params=zlib_params, ppmd_params=ppmd_params)
            cxy, txy = zlib_ppmd_timed_compress_len((x+y), zlib_params=zlib_params, ppmd_params=ppmd_params)
            processing_time += tx + ty + txy
    else:
        for i in range(rounds):
            cx, tx = ppmd_zlib_timed_compress_len(x, zlib_params=zlib_params, ppmd_params=ppmd_params)
            cy, ty = ppmd_zlib_timed_compress_len(y, zlib_params=zlib_params, ppmd_params=ppmd_params)
            cxy, txy = ppmd_zlib_timed_compress_len((x+y), zlib_params=zlib_params, ppmd_params=ppmd_params)
            processing_time += tx + ty + txy

    processing_time /= rounds

    return (cxy - min(cx, cy))/max(cx, cy), processing_time

def zlib_ppmd_get_data_and_time(
      data_dir1:str, 
      data_dir2:str, 
      n_files:int, 
      zlib_params = [zlib.Z_BEST_COMPRESSION, zlib.DEFLATED, zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, zlib.Z_DEFAULT_STRATEGY],
      ppmd_params = [12, 512<<10, "I"],
      rounds=5,
      zlib_first=True):
  
  # Abre os arquivos 10 arquivos do tipo PROCESS e CONTROL.
    try:
        print(f"Opening {n_files} files from {data_dir1}..")
        data1 = open_files_from_dir(data_dir1, n_files)
        process_tam = len(data1)

        print(f"Opening {n_files} files from {data_dir2}...")
        data2 = open_files_from_dir(data_dir2, n_files) # Open the first set of compressed files
        control_tam = len(data2)

    except Exception as e:
        print("ERROR: an error happened while opening files from directories")

    # Filtra o nome dos arquivos PROCESS para manter apenas o necessário.
    x_axis = []
    for i in range(process_tam):
        filename = data1[i][1]
        filename = filename.replace("dtc_experiment_code_","").replace("_py","").replace("_csv","")
        x_axis.append(filename)

    ncd_results = [] # Lista que contém os datasets de NCD para gerar o gráfico posteriormente.

    print(f"Teste -> ZLIB e PPMd")
    ncd_values = [] # Lista que contém os valores de NCD defeito-defeito e defeito-não-defeito.
    ar_deflect = [] # Lista que contém os valores de NCD defeito-defeito.
    ar_non_deflect = [] # Lista que contém os valores de NCD defeito-não-defeito.

    processing_time = 0 # Variável para o tempo de processamento.
    ncd_dif = 0 # Variável para a média da diferença absoluta entre as NCDs da comparação de cada arquivo.

    for i in range(n_files): # Laço para cada arquivo defeituoso (PROCESS)
        deflect_average = 0
        non_deflect_average = 0

        for j in range(n_files): # Laço para cada arquivo defeituoso (PROCESS) e não-defeituoso (CONTROL).
            if i != j:
                ncd, time = zlib_and_ppmd_timed_ncd(data1[i][0], data1[j][0], zlib_params=zlib_params, ppmd_params=ppmd_params, rounds=rounds, zlib_first=zlib_first) # Calcula a NCD entre PROCESS-PROCESS.
                #print(f"NCD 1 ({data1[i][1]} x {data1[j][1]}): {ncd}")
                deflect_average += ncd # Incrementa a média da NCD do tipo defeito.
                processing_time += time # Incrementa o tempo de processamento.

            ncd, time = zlib_and_ppmd_timed_ncd(data1[i][0], data2[j][0], zlib_params=zlib_params, ppmd_params=ppmd_params, rounds=rounds, zlib_first=zlib_first) # Calcula a NCD entre PROCESS-CONTROL
            
            #print(f"NCD 2: {ncd}")
            non_deflect_average += ncd # Incrementa a média da NCD do tipo não-defeito.
            processing_time += time # Incrementa o tempo de processamento.

        deflect_average /= n_files - 1 # Finaliza a média da NCD do tipo defeito.
        ar_deflect.append(deflect_average)

        non_deflect_average /= n_files # Finaliza a média da NCD do tipo não-defeito
        ar_non_deflect.append(non_deflect_average)

        ncd_dif += non_deflect_average - deflect_average # Calcula a diferença entre as NCDs.

    ncd_values.append(ar_deflect)
    ncd_values.append(ar_non_deflect)
    ncd_dif /= n_files # Finaliza a média das diferenças absolutas.

    ncd_results.append((processing_time, ncd_dif, ncd_values)) # Armazena um dataset para um gráfico.
    return ncd_results, x_axis

if __name__ == "__main__":
    process_dir = "../data/LARGEST/PROCESS"
    control_dir = "../data/LARGEST/CONTROL"

    dataset, x_axis = zlib_ppmd_get_data_and_time(process_dir, control_dir, 10, rounds=5, zlib_first=True)

    zlib_ppmd_print_all_graphs(dataset, x_axis, title="ZLIB first")

    dataset, x_axis = zlib_ppmd_get_data_and_time(process_dir, control_dir, 10, rounds=5, zlib_first=False)

    zlib_ppmd_print_all_graphs(dataset, x_axis, title="PPMd first")