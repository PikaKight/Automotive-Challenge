#!/usr/bin/env python
import os

from ultralytics import YOLO, settings

def setup():
    cwd = os.getcwd()

    data_dir = settings.get("datasets_dir")

    if cwd is data_dir:
        print("same")
        return

    settings.update({"datasets_dir": cwd})

def parking_model(yaml_path: str, save_path: str):

    model = YOLO("yolo11n.pt", task="detect")

    model.train(data=yaml_path, epochs=50, imgsz=640)

    model.save(save_path)

def parking_metrics(model_path, yaml_path):
    model = YOLO(model_path)
    
    metrics = model.val(data=yaml_path)

    avg_precision = metrics.box.mp

    avg_recall = metrics.box.mr

    f1 = 2 * ((avg_precision * avg_recall) / (avg_precision + avg_recall))

    print(f"""
    
        Avg Precision: {avg_precision}

        Avg Recall: {avg_recall}

        Avg F1: {f1}
          """)


def parking_pred(model_path: str, tests: list):
    model = YOLO(model_path)

    pred = model(tests, conf=0.2)


    results = {}

    for img in pred:
        img_name = img.path.split('/')[3]
        img.save_txt(f"resources/test/test_res/{img_name}.txt")
        results[img_name] = []

        for box in img.boxes:
            res = box.xyxy[0].tolist()
            status = box.cls[0].tolist()

            res.insert(0, status)

            results[img_name].append(res)
    
    return results

if __name__ == "__main__":

    import json

    path = "backend/model/parking.yaml"
    
    setup()

    model_path = "backend/model/parking.pt"

    if not os.path.exists(model_path):
        parking_model(path, model_path)

        parking_metrics(model_path, path)

    test = "resources/test/test_images/"

    tests = [os.path.join(test, f) for f in os.listdir(test)]

    res = parking_pred(model_path, tests)

    with open("resources/test/test_res/test.json", 'w') as f:
        json.dump(res, f, indent=4)
