import pyppmd
from graphs import *
from support import *
from time import process_time

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

def ppmd_timed_ncd(
        x:bytes, 
        y:bytes, 
        order=6, 
        mem_size = 32<<10, 
        variant="I", 
        rounds=1) -> tuple[float, float]:
    def timed_compress_len(data:bytes, order=6, mem_size = 32<<10, variant="I") -> tuple[float,float]:
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

def ppmd_get_data_and_time(
      data_dir1:str, 
      data_dir2:str, 
      n_files:int, 
      orderset = [6], 
      memset = [32], 
      rounds = 5):
  
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

    for mem in memset:
        for order in orderset:
            print(f"Teste -> Ordem: {order}; Tamanho de memória:{mem}")
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
                        ncd, time = ppmd_timed_ncd(data1[i][0], data1[j][0], order=order, mem_size=mem<<10,rounds=rounds) # Calcula a NCD entre PROCESS-PROCESS.
                        #print(f"NCD 1 ({data1[i][1]} x {data1[j][1]}): {ncd}")
                        deflect_average += ncd # Incrementa a média da NCD do tipo defeito.
                        processing_time += time # Incrementa o tempo de processamento.

                    ncd, time = ppmd_timed_ncd(data1[i][0], data2[j][0], order=order, rounds=rounds) # Calcula a NCD entre PROCESS-CONTROL
                    
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

            ncd_results.append((order, mem, processing_time, ncd_dif, ncd_values)) # Armazena um dataset para um gráfico.
    return ncd_results, x_axis

if __name__ == "__main__":
    process_dir = "../data/LARGEST/PROCESS"
    control_dir = "../data/LARGEST/CONTROL"

    # print(f"Opening {5} files from {process_dir}..")
    # data1 = open_files_from_dir(process_dir, 5)

    # print(f"Opening {5} files from {control_dir}...")
    # data2 = open_files_from_dir(control_dir, 5) # Open the first set of compressed files
    
    # ncd = ppmd_ncd_original_data(data2[0][0], data2[0][0], order=6, mem_size=512<<10)
    # print(f"ncd = {ncd} - {data2[0][1]} x {data2[0][1]}")

    dataset, x_axis = ppmd_get_data_and_time(process_dir, control_dir, 10, [12], [512], rounds=5)

    ppmd_print_all_graphs(dataset, x_axis)