#!/usr/bin/env python
import os
import shutil

from parse import parse_lines

PATH = "resources/training"


def split_train_val():

    train = parse_lines(PATH, "train_labels.txt", "train_images")

    val = parse_lines(PATH, "val_labels.txt", "val_images")
    
    copy_files(f"{PATH}/train_images", f"{PATH}/images/train", train.keys())
    copy_files(f"{PATH}/val_images", f"{PATH}/images/val", val.keys())
    
    make_labels("train", train.keys(), train)
    make_labels("val", val.keys(), val)

def copy_files(folder: str, file_path: str, images: list):
    if os.path.exists(file_path):
        shutil.rmtree(file_path)

    os.makedirs(file_path)

    for image in images:
        path = os.path.join(folder, image)
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
    split_train_val()