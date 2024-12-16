import timeit
from tqdm import tqdm
import numpy as np
import csv
from compressors import *
from compressing import *
from create_tests import *

if __name__ == "__main__":

  compressors = ["gzip", "zlib", "bz2"]

  with open('../results/compression_times.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Compressor", "Min Time", "Max Time", "Mean Time", "Std Time"])

    for compressor in tqdm(compressors, desc="Running test for all compressors"):
      stmt = f'create_ncd_mixed_matrix("../data/LARGE/PROCESS/", 10, "../data/LARGE/CONTROL/", 10, "../results/", "{compressor}")'
      setup = 'from __main__ import create_ncd_mixed_matrix'
      times = []

      for _ in tqdm(range(15000), desc=f"Running repeats for {compressor}"):
        timer = timeit.Timer(stmt=stmt, setup=setup)
        times.append(timer.timeit(number=1))
      
      min_time = np.min(times)
      max_time = np.max(times)
      mean_time = np.mean(times)
      std_time = np.std(times)
      
      writer.writerow([compressor, min_time, max_time, mean_time, std_time])