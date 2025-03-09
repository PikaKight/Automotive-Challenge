#!/usr/bin/env python
import os

from ultralytics import YOLO, settings

def setup():
    """ Sets up the working directory for the YOLO model to find the dataset
    """
    cwd = os.getcwd()

    data_dir = settings.get("datasets_dir")

    # Checks if the current working directory is the same as dataset directory
    if cwd is data_dir:
        print("same")
        return

    settings.update({"datasets_dir": cwd})

def parking_model(yaml_path: str, save_path: str):
    """Creates a YOLO model and trains it

    Args:
        yaml_path (str): The yaml file that holds the instruction for the YOLO model to get the dataset
        save_path (str): The location where the trained model is saved
    """

    model = YOLO("yolo11n.pt", task="detect")

    model.train(data=yaml_path, epochs=50, imgsz=640)

    model.save(save_path)

def parking_metrics(model_path: str, yaml_path: str):
    """Validates the model

    Args:
        model_path (str): The location of the model
        yaml_path (str): The yaml file path that holds the instruction for the YOLO model
    """

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


def parking_pred(model_path: str, tests: list) -> dict:
    """Identifies the parking space vacancies for a given list of images

    Args:
        model_path (str): The location of the model
        tests (list): A list of image paths

    Returns:
        dict: The result of the identification
    """
    model = YOLO(model_path)

    pred = model(tests, conf=0.2)

    results = {}

    # Loops through the results of the model
    for img in pred:
        
        # Gets the image file name 
        img_name = img.path.split('/')[3]

        # Saves the result of the identification of the image as a txt file
        img.save_txt(f"resources/test/test_res/{img_name}.txt")
        
        # Used to store the result of the identification 
        results[img_name] = []

        # Loops through each object in the image that has a
        # bound box that shows the identification
        for box in img.boxes:
            # Gets the position of the box
            res = box.xyxy[0].tolist()

            # Gets the status (vacancy) of the spot
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
