from compressors import *
from compressing import *
from create_tests import *

data_path = "../data/"
compressed_data_path = "../compressed_data/"
compressor = "gzip"

if __name__ == "__main__":
    # compress_all_from_dir("../data/LARGE/PROCESS/", "../compressed_data/LARGE/PROCESS/", compressor)
    # compress_all_from_dir("../data/LARGE/CONTROL/", "../compressed_data/LARGE/CONTROL/", compressor)
    compress_all_from_dir("../data/LARGE/CONTROL/", "../compressed_data/LARGE/CONTROL/", "ppmd")    

    # -----------------------------------------------------------------------------------------

    # remove_redundant_data("../data/LARGE/PROCESS/", "../data/LARGE/PROCESS/non_redundant/")
    # remove_redundant_data("../data/LARGE/CONTROL/", "../data/LARGE/CONTROL/non_redundant/")
    # remove_redundant_data("../data/LARGE/MEMORY/", "../data/LARGE/MEMORY/non_redundant/")
    # remove_redundant_data("../data/LARGE/TRAIN/", "../data/LARGE/TRAIN/non_redundant/")
    
    # -----------------------------------------------------------------------------------------

    # # Create the NCD matriz mixing PROCESS files and CONTROL files.
    # create_ncd_mixed_matrix("../data/LARGE/PROCESS/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/PROCESS", "zlib")
    # create_ncd_mixed_matrix("../data/LARGE/PROCESS/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/PROCESS", "gzip")
    # create_ncd_mixed_matrix("../data/LARGE/PROCESS/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/PROCESS", "bz2")
    create_ncd_mixed_matrix("../data/LARGE/PROCESS/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/PROCESS", "ppmd")

    # # Create the NCD matriz mixing MEMORY files and CONTROL files.
    # create_ncd_mixed_matrix("../data/LARGE/MEMORY/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/MEMORY", "zlib")
    # create_ncd_mixed_matrix("../data/LARGE/MEMORY/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/MEMORY", "gzip")
    # create_ncd_mixed_matrix("../data/LARGE/MEMORY/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/MEMORY", "bz2")
    create_ncd_mixed_matrix("../data/LARGE/MEMORY/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/MEMORY", "ppmd")

    # # Create the NCD matriz mixing TRAIN files and CONTROL files.
    # create_ncd_mixed_matrix("../data/LARGE/TRAIN/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/TRAIN", "zlib")
    # create_ncd_mixed_matrix("../data/LARGE/TRAIN/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/TRAIN", "gzip")
    # create_ncd_mixed_matrix("../data/LARGE/TRAIN/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/TRAIN", "bz2")
    create_ncd_mixed_matrix("../data/LARGE/TRAIN/", 10, "../data/LARGE/CONTROL/", 10, "../results/LARGE/TRAIN", "ppmd")

    # -----------------------------------------------------------------------------------------

    # nr_proc_path = "../data/LARGE/PROCESS/non_redundant"
    # nr_con_path = "../data/LARGE/CONTROL/non_redundant/"
    # nr_result_proc_path = "../results/LARGE/PROCESS/non_redundant"

    # # Create the NCD matriz mixing PROCESS non redundant files and CONTROL non redundant files.
    # create_ncd_mixed_matrix(nr_proc_path, 10, nr_con_path, 10, nr_result_proc_path, "zlib")
    # create_ncd_mixed_matrix(nr_proc_path, 10, nr_con_path, 10, nr_result_proc_path, "ppmd")
    # create_ncd_mixed_matrix(nr_proc_path, 10, nr_con_path, 10, nr_result_proc_path, "gzip")
    # create_ncd_mixed_matrix(nr_proc_path, 10, nr_con_path, 10, nr_result_proc_path, "bz2")

    # nr_mem_path = "../data/LARGE/MEMORY/non_redundant"
    # nr_result_mem_path = "../results/LARGE/MEMORY/non_redundant"

    # # Create the NCD matriz mixing MEMORY non redundant files and CONTROL non redundant files.
    # create_ncd_mixed_matrix(nr_mem_path, 10, nr_con_path, 10, nr_result_mem_path, "zlib")
    # create_ncd_mixed_matrix(nr_mem_path, 10, nr_con_path, 10, nr_result_mem_path, "ppmd")
    # create_ncd_mixed_matrix(nr_mem_path, 10, nr_con_path, 10, nr_result_mem_path, "gzip")
    # create_ncd_mixed_matrix(nr_mem_path, 10, nr_con_path, 10, nr_result_mem_path, "bz2")

    # nr_train_path = "../data/LARGE/TRAIN/non_redundant"
    # nr_result_train_path = "../results/LARGE/TRAIN/non_redundant"

    # # Create the NCD matriz mixing MEMORY non redundant files and CONTROL non redundant files.
    # create_ncd_mixed_matrix(nr_train_path, 10, nr_con_path, 10, nr_result_train_path, "zlib")
    # create_ncd_mixed_matrix(nr_train_path, 10, nr_con_path, 10, nr_result_train_path, "ppmd")
    # create_ncd_mixed_matrix(nr_train_path, 10, nr_con_path, 10, nr_result_train_path, "gzip")
    # create_ncd_mixed_matrix(nr_train_path, 10, nr_con_path, 10, nr_result_train_path, "bz2")


