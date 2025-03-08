import os
import shutil
import random

PATH = "./resources"

def split_train_val_test():
    images_path = f"{PATH}/test_images"