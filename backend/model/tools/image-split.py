#!/usr/bin/env python

import os
import shutil
import random

from parse import parse_lines

PATH = "../resources"

IMG_PATH = f"{PATH}/test_images"

TRAIN_PATH = f"{PATH}/images/Train"
VAL_PATH = f"{PATH}/images/Validation"
TEST_PATH = f"{PATH}/images/Test"

SEED = 42

# 70% Train, 15% Validation, 15% Test
SPLIT_AMOUNT = [0.7, 0.15, 0.15]

def split_train_val_test():

    data_set = parse_lines(PATH, "test_labels.txt", "test_images")

    images = [i for i in data_set.keys()]

    random.seed(SEED)
    random.shuffle(images)

    num_img = len(images)

    train_split_i = int(SPLIT_AMOUNT[0] * num_img)

    val_split_i = int((SPLIT_AMOUNT[1] + SPLIT_AMOUNT[0]) * num_img)

    train_split = images[:train_split_i]
    val_split = images[train_split_i: val_split_i]
    test_split = images[val_split_i:]

    move_files(TRAIN_PATH, train_split)
    move_files(VAL_PATH, val_split)
    move_files(TEST_PATH, test_split)

    make_labels("Train", train_split, data_set)
    make_labels("Val", val_split, data_set)
    make_labels("Test", test_split, data_set)


def move_files(file_path: str, images: list):
    shutil.rmtree(file_path)

    os.makedirs(file_path)

    for image in images:
        path = os.path.join(IMG_PATH, image)
        shutil.copy(path, file_path)
    

def make_labels(cat:str, images: list, dataset: dict):

    label_dir = f"{PATH}/labels/{cat}"

    if os.path.exists(label_dir):
        shutil.rmtree(label_dir)

    os.makedirs(label_dir)

    for image in images:

        path = os.path.splitext(image)[0]

        with open(f"{label_dir}/{path}.txt", 'w+') as f:
            for data in dataset[image]:
                f.write(' '.join(data) + '\n')


if __name__ == "__main__":
    split_train_val_test()