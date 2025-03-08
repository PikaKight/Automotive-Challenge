import os
import shutil
import random

from tools.parse import parse_lines

PATH = "./resources"

images_path = f"{PATH}/test_images"

def split_train_val_test():
    
    data_set = parse_lines(f"{PATH}/test_labels.txt")

    print(data_set)


if __name__ == "__main__":
    split_train_val_test()