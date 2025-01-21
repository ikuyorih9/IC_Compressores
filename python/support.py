import os

def mix_bytes(x: bytes, y: bytes, chunk_size: int) -> bytes:
    """
    Intercala os bytes de dois streams em blocos de tamanho chunk_size.

    Parâmetros:
    - x: bytes do primeiro arquivo.
    - y: bytes do segundo arquivo.
    - chunk_size: tamanho do bloco de intercalação. Se `chunk_size=-1`, não há mesclagem de bytes.

    Retorno:
    - Um único stream de bytes com os dados de x e y intercalados em blocos de chunk_size. Se `chunk_size=-1`, retorna a concatenação `x+y` bytes.
    """
    if chunk_size == -1:
        return x+y

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

            print(f"\tOpening file {rpath}...")

            with open(rpath, 'rb') as file: # Open the file.
                data = file.read() # Read the file.
                datalist.append((data, filename)) # Append to the return list.

            cont += 1
        return datalist # Return the data list.
    except FileNotFoundError as fnfe:
        print(f"ERROR: {fnfe}")
        return None
    
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

def create_non_redundant_files(rootpath:str):
    for dir in os.listdir(rootpath):
        inner_path = os.path.join(rootpath, dir)
        outer_path = os.path.join(rootpath, dir + '_zero')

        remove_redundant_data(inner_path, outer_path)

def remove_all_files(diretorio:str):
    try:
        # Lista todos os itens no diretório
        itens = os.listdir(diretorio)
        
        for item in itens:
            caminho_completo = os.path.join(diretorio, item)  # Cria o caminho completo
            
            # Verifica se é um arquivo e o remove
            if os.path.isfile(caminho_completo):
                os.remove(caminho_completo)
                print(f"Arquivo removido: {caminho_completo}")
            elif os.path.isdir(caminho_completo):
                print(f"'{caminho_completo}' é um diretório. Ignorando.")
    except FileNotFoundError:
        print(f"O diretório '{diretorio}' não foi encontrado.")
    except PermissionError:
        print(f"Permissão negada para acessar o diretório '{diretorio}'.")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

def merge_files(dir:str, num_files:int, out_names:str = "merged"):
    i = 1
    group = 0
    files = []
    files.append("")

    print(f"Lendo arquivos do grupo {group}")
    for filename in os.listdir(dir):
        in_path = os.path.join(dir, filename)
        if os.path.isdir(in_path):
            print(f"{filename} é um diretório. Ignorando...")
            continue

        
        print(f"\t{filename}")
        
        with open(in_path, "r") as in_file:
            file_data = in_file.read()
            files[group] += file_data

        if i%num_files == 0:
            files.append("")
            group += 1
            print(f"Lendo arquivos do grupo {group}")
        
        i += 1
    
    out_path = os.path.join(dir, "merged")
    remove_all_files(out_path)

    if not os.path.exists(out_path): # If the output path doesn't exist
        print(f"\tDirectory {out_path} doesn't exist. Creating...")
        os.makedirs(out_path, exist_ok=True) # Create the output path.

    for i in range(len(files)-1):
        final_path = os.path.join(out_path, out_names + '_' + str(i))

        with open(final_path, "w") as out_file:
            out_file.write(files[i])
            
if __name__ == "__main__":
    # create_non_redundant_files("../data/LARGEST/")
    merge_files("../data/LARGEST/PROCESS_zero", 6, "process")
    merge_files("../data/LARGEST/CONTROL_zero", 6, "control")