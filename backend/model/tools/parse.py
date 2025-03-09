#!/usr/bin/env python

from PIL import Image

def parse_lines(folder_path, file, folder):
    parsed_data = {}
    
    with open(f"{folder_path}/{file}", 'r') as file:
        for line in file:
            parts = line.strip().split()
            key = parts[0]
            values = list(map(float, parts[1:]))  # Convert numbers to float
            
            if values[0] == 2:
                values[0] = '1'
            else:
                values[0] = '0'

            ## Normalization
            img = Image.open(f"{folder_path}/{folder}/{key}")
            img_Width, img_Height = img.size

            min_x = values[1]
            min_y = values[2]
            max_x = values[3]
            max_y = values[4]

            xc = ((min_x+max_x) / 2) / img_Width
            yc = ((min_y+max_y) / 2) / img_Height
            width = (max_x - min_x) / img_Width
            height = (max_y - min_y) / img_Height

            values[1] = str(xc)
            values[2] = str(yc)
            values[3] = str(width)
            values[4] = str(height)


            if key in parsed_data:
                parsed_data[key].append(values)
            else:
                parsed_data[key] = [values]
    
    return parsed_data



if __name__ == "__main__":
# Example usage
    file_path = "resources/test_labels.txt"  # Replace with your actual file path
    data = parse_lines(file_path)
