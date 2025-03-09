#!/usr/bin/env python
import cv2

def to_txt(results: dict, dest: str):
    """Turns the results of the model to a single txt file

    Args:
        results (dict): The results of the model
        dest (str): The file path where the txt file should be stored
    """
    lines = []

    for img in results.keys():
        
        for lot in results[img]:

            # Transforms the vacancy into the required formate            
            match lot[0]:

                case 0.0:
                    lot[0] = 1
                case 1.0:
                    lot[0] = 2

            line = f"{img} {lot[0]} {lot[1]} {lot[2]} {lot[3]} {lot[4]}\n"
            
            lines.append(line)
    
    with open(dest, 'w') as f:
        f.writelines(lines)

def draw_boxes(results: dict, folder_path: str, dest_path: str) -> None:
    """Draws the boxes on the images

    Args:
        results (dict): The results of the model
        folder_path (str): The location of the images
        dest_path (str): The destination path

    """
    thickness = 2

    for img in results.keys():
        
        image = cv2.imread(f"{folder_path}/{img}")

        for lot in results[img]:
            
            # Sets the color of the box based on the vacancy
            match lot[0]:
                case 1:
                    color = (0,255,0) # Green for vacant
                    text = "Vacant"
                    
                case 2:
                    color = (0, 0, 255) # Red for occupied
                    text = "Occupied"
            
            # Sets the start and end points of the box
            start = (int(lot[1]), int(lot[2]))
            end = (int(lot[3]), int(lot[4]))

            # Draws the rectangle and adds a text
            cv2.rectangle(image, start, end, color, thickness)
            cv2.putText(image, text, (int(lot[1]), int(lot[4]) + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, color)
        
        cv2.imwrite(f"{dest_path}/{img}", image)            


if __name__ == "__main__":
    import json

    window_name = "Parking Availability"

    with open("resources/test/test_res/test.json", 'r') as f:
        res = json.load(f)

    to_txt(res, "resources/test/test_res/results.txt")

    draw_boxes(res, "resources/test/test_images", "resources/test/test_dest")

