#!/usr/bin/env python

from ultralytics import YOLO

def parking_model(yaml_path: str):

    model = YOLO("yolo11n.pt")

    model.train(data=yaml_path, epochs=50)

if __name__ == "__main__":
    path = "model/parking.yaml"

    parking_model(path)