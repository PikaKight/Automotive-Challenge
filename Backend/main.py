#!/usr/bin/env python

import cv2
import os
import argparse

from model.parking import parking_pred
from model.tools.handle_pred import to_txt

MODEL = "backend/model/parking.pt"

parser = argparse.ArgumentParser(description="Run solution")
parser.add_argument("--image_folder", action="image_folder", type=str, help="Image Folder path")
parser.add_argument("--results_folder", action="results_folder, type=str, help="Result folder path")
args = parser.parse_args()


img_folder = args.image_folder
res_folder = args.results_folder

imgs = []

for d, dn, files in os.walk(img_folder):
    for file in files:
        imgs.append(f"{img_folder}/{file}")

res = parking_pred(MODEL, imgs)

to_txt(res, f"{res_folder}/results.txt")

