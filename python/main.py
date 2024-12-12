from compressors import *
from compressing import *
from create_tests import *

data_path = "../data/"
compressed_data_path = "../compressed_data/"

if __name__ == "__main__":
    # rotate_some_bytes_from_dir(data_path + "LITTLE_PRINCE/", 1, ['a', 'e', 'o'])
    # rotate_some_bytes_from_dir(data_path + "LITTLE_PRINCE/", 1, ['b', 'h', 'f'])
    # rotate_all_bytes_from_dir(data_path + "LITTLE_PRINCE/", 1)
    
    # compress_all_from_dir("../data/LITTLE_PRINCE/", "../compressed_data/LITTLE_PRINCE/", "zlib")
    # compress_all_from_dir("../data/LITTLE_PRINCE/", "../compressed_data/LITTLE_PRINCE/", "bz2")
    compress_all_from_dir("../data/LITTLE_PRINCE/", "../compressed_data/LITTLE_PRINCE/", "gzip")