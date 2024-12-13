from compressors import *
from compressing import *
from create_tests import *

data_path = "../data/"
compressed_data_path = "../compressed_data/"
compressor = "bz2"

if __name__ == "__main__":
    compress_all_from_dir("../data/LARGE/PROCESS/", "../compressed_data/LARGE/PROCESS/", compressor)
    compress_all_from_dir("../data/LARGE/CONTROL/", "../compressed_data/LARGE/CONTROL/", compressor)

    create_ncd_mixed_matrix("../compressed_data/LARGE/PROCESS/", 10, "../compressed_data/LARGE/CONTROL/", 10, "../results/", compressor)