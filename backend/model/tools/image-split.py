#!/usr/bin/env python
import os
import shutil

from parse import parse_lines

PATH = "resources/training"


def split_train_val():
    """Splits the images into the train and val and makes the labels
    """

    train = parse_lines(PATH, "train_labels.txt", "train_images")

    val = parse_lines(PATH, "val_labels.txt", "val_images")
    
    copy_files(f"{PATH}/train_images", f"{PATH}/images/train", train.keys())
    copy_files(f"{PATH}/val_images", f"{PATH}/images/val", val.keys())
    
    make_labels("train", train.keys(), train)
    make_labels("val", val.keys(), val)

def copy_files(folder: str, file_path: str, images: list):
    """Copies the images to their respective folders

    Args:
        folder (str): Folder location where the images are held
        file_path (str): The target folder location
        images (list): The list of image paths
    """

    # Checks if the folder already exists
    if os.path.exists(file_path):

        # Deletes the folder
        shutil.rmtree(file_path)

    # Creates the target folder location
    os.makedirs(file_path)

    # Copies over the images
    for image in images:
        path = os.path.join(folder, image)
        shutil.copy(path, file_path)
    

def make_labels(cat:str, images: list, dataset: dict):
    """Separates the labels from the general label txt into individual txt for each image

    Args:
        cat (str): The type of label its used for (train, val)
        images (list): List of the image paths
        dataset (dict): The dataset
    """
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