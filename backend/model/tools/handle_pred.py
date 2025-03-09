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

def draw_boxes(results: dict, folder_path: str) -> list:
    """Draws the boxes on the images

    Args:
        results (dict): The results of the model
        folder_path (str): The location of the images

    Returns:
        list: A list of OpenCV Images that has the boxes drawn
    """
    thickness = 2

    images = []

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
        
        images.append(image)

    return images

if __name__ == "__main__":
    import json

    window_name = "Parking Availability"

    with open("resources/test/test_res/test.json", 'r') as f:
        res = json.load(f)

    to_txt(res, "resources/test/test_res/results.txt")

    images = draw_boxes(res, "resources/test/test_images")

    for img in images:
        cv2.imshow(window_name, img)

        cv2.waitKey(0)

        cv2.destroyAllWindows()
