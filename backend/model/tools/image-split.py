#!/usr/bin/env python

import os
import shutil
import random

from parse import parse_lines

PATH = "../resources"

IMG_PATH = f"{PATH}/test_images"

TRAIN_PATH = f"{PATH}/Train"
VAL_PATH = f"{PATH}/Validation"
TEST_PATH = f"{PATH}/Test"

SEED = 42

# 70% Train, 15% Validation, 15% Test
SPLIT_AMOUNT = [0.7, 0.15, 0.15]

def split_train_val_test():

    data_set = parse_lines(f"{PATH}/test_labels.txt")

    images = [i for i in data_set.keys()]

    random.seed(SEED)
    random.shuffle(images)

    num_img = len(images)

    train_split = int(SPLIT_AMOUNT[0] * num_img)

    val_split = int((SPLIT_AMOUNT[1] + SPLIT_AMOUNT[0]) * num_img)

    move_files(TRAIN_PATH, images[:train_split])
    move_files(VAL_PATH, images[train_split: val_split])
    move_files(TEST_PATH, images[val_split:])


def move_files(file_path: str, images: list):
    shutil.rmtree(file_path)

    os.makedirs(file_path)

    for image in images:
        path = os.path.join(IMG_PATH, image)
        shutil.copy(path, file_path)
    

if __name__ == "__main__":
    split_train_val_test()