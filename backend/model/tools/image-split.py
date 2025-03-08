#!/usr/bin/env python

import json
import random

from parse import parse_lines

PATH = "../resources"

IMG_PATH = f"{PATH}/test_images"

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

    split = {
        "Train": images[:train_split],
        "Validation": images[train_split: val_split],
        "Test": images[val_split:]
    }

    response = {
        "Splits": split,
        "Data": data_set 
    }

    return response

if __name__ == "__main__":
    res = split_train_val_test()

    with open(f"{PATH}/test.json", "w") as f:
        json.dump(res, f, indent=4)