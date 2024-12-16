from compressors import *
from compressing import *
from create_tests import *

import cProfile
from tqdm import tqdm  # Adicione a importação da biblioteca tqdm
import subprocess  # Adicione a importação do subprocess

def prof_test(x : int, compressor):
  for _ in tqdm(range(x), desc=f"Running {compressor} tests"):
    create_ncd_mixed_matrix("../data/LARGE/PROCESS/", 10, "../data/LARGE/CONTROL/", 10, "../results/", compressor)

if __name__ == "__main__":
  quantity = 1000

  compressors = {"gzip", "zlib", "bz2"}

  for compressor in compressors:
    stats_file = f"../results/{compressor}/{compressor}.stats"
    # cProfile.run('prof_test(quantity, compressor)', stats_file)
    cProfile.run(f'create_ncd_mixed_matrix("../data/LARGE/PROCESS/", 10, "../data/LARGE/CONTROL/", 10, "../results/", "{compressor}")', stats_file)
    # Gera a imagem PNG usando gprof2dot e dot
    subprocess.run(f'gprof2dot -f pstats {stats_file} | dot -Tpng -o ../results/{compressor}/{compressor}.png', shell=True)
