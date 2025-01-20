"""
Funções de compressão com o compressor ZLIB.
"""

import zlib
from graphs import *
from support import *
from time import process_time

def zlib_compress(data: bytes) -> bytes:
    return zlib.compress(data)

def zlib_compressed_size(
        data: bytes, 
        level = zlib.Z_BEST_COMPRESSION, 
        method = zlib.DEFLATED, 
        wbits = zlib.MAX_WBITS, 
        memLevel = zlib.DEF_MEM_LEVEL, 
        strategy = zlib.Z_FILTERED) -> int:
    compressor = zlib.compressobj(
        level=level,  # Nível de compressão (0 a 9)
        method=method,           # Método de compressão (DEFLATED é padrão)
        wbits=wbits,           # Tamanho da janela (máximo é 15)
        memLevel=memLevel,    # Uso de memória (1 a 9, padrão: 8)
        strategy=strategy  # Estratégia de compressão
    )
    return len(compressor.compress(data)+ compressor.flush())

def zlib_ncd_original_data(
        x:bytes, 
        y:bytes, 
        level = zlib.Z_BEST_COMPRESSION, 
        method = zlib.DEFLATED, 
        wbits = zlib.MAX_WBITS, 
        memLevel = zlib.DEF_MEM_LEVEL, 
        strategy = zlib.Z_FILTERED) -> float:
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

def zlib_timed_ncd(
        x:bytes, 
        y:bytes, 
        level = zlib.Z_BEST_COMPRESSION, 
        method = zlib.DEFLATED, 
        wbits = zlib.MAX_WBITS, 
        memLevel = zlib.DEF_MEM_LEVEL, 
        strategy = zlib.Z_DEFAULT_STRATEGY, 
        rounds = 10, 
        chunk_size = -1) -> tuple[float, float]:
    """
    Calculates NCD from non compressed data X and Y using ZLIB compressor and gets the processing time.

    Args:
        x (bytes): bytes from original file 1.
        y (bytes): bytes from original file 2.
        level: number of level of compression parameter (0 to 9).
        method: number that represents which method compressor uses. Only supports zlib.DEFLATED.
        wbits: number that represents the size of sliding window.
        strategy: number that represents the strategy of compressiong.
        rounds: number of testing rounds.
        chunk_size: chunk size for the mix block between x and y.
    
    Returns:
        [float, float]: the NCD value and the processing time.
    """
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

def zlib_get_data_and_time(
        data_dir1:str,
        data_dir2:str,
        n_files:int,
        levelset = [zlib.Z_BEST_COMPRESSION], 
        windowset = [zlib.MAX_WBITS], 
        memset = [zlib.DEF_MEM_LEVEL], 
        strategyset=[zlib.Z_DEFAULT_STRATEGY], 
        chunk_size=-1,
        rounds = 1):

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

    strategy_dict = {
        zlib.Z_DEFAULT_STRATEGY: "Deflate",
        zlib.Z_FILTERED: "Filtered",
        zlib.Z_HUFFMAN_ONLY: "Huffman Only",
        zlib.Z_RLE: "RLE",
        zlib.Z_FIXED: "Fixed"
    }

    for strategy in strategyset:
        for mem in memset:
            for window_size in windowset:
                for level in levelset:
                    print(f"Teste -> Nível: {level}; Tamanho de memória:{mem}; Tamanho da janela: {window_size}; Estratégia: {strategy_dict[strategy]}")
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
                                ncd, time = zlib_timed_ncd(data1[i][0], data1[j][0], level=level, wbits=window_size, memLevel=mem, strategy=strategy, rounds=rounds, chunk_size=chunk_size) # Calcula a NCD entre PROCESS-PROCESS.
                                deflect_average += ncd # Incrementa a média da NCD do tipo defeito.
                                processing_time += time # Incrementa o tempo de processamento.

                            ncd, time = zlib_timed_ncd(data1[i][0], data2[j][0], level=level, wbits=window_size, memLevel=mem, strategy=strategy, rounds=rounds, chunk_size=chunk_size) # Calcula a NCD entre PROCESS-CONTROL
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

                    ncd_results.append(((level, window_size, mem, strategy_dict[strategy]), processing_time, ncd_dif, ncd_values)) # Armazena um dataset para um gráfico.

    return ncd_results, x_axis

if __name__ == "__main__":
    process_dir = "../data/LARGEST/PROCESS_zero"
    control_dir = "../data/LARGEST/CONTROL_zero"

    dataset, x_axis = zlib_get_data_and_time(process_dir, control_dir, 10, chunk_size=512, rounds=10)

    zlib_print_all_graphs(dataset, x_axis)