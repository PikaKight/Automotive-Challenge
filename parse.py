import re

# Initialize lists to store unique file names, status, and coordinates
unique_files = []
status = []
coordinates = []

# Open the file in read mode
with open(r'C:\Users\aaqil\Downloads\parking_dataset\train_labels.txt', 'r') as file:
    for line in file:
        # Simplified regular expression to match file name, status, and four coordinates
        match = re.match(r'([a-zA-Z0-9_-]+\.jpg)\s(\d+)\s(\d+\.\d+|\d+)\s(\d+\.\d+|\d+)\s(\d+\.\d+|\d+)\s(\d+\.\d+|\d+)', line)
        
        if match:
            file_name = match.group(1)  # Capture the filename
            digit1 = int(match.group(2))  # Capture the status
            coords = [
                float(match.group(3)),  # First coordinate
                float(match.group(4)),  # Second coordinate
                float(match.group(5)),  # Third coordinate
                float(match.group(6))   # Fourth coordinate
            ]  # Four coordinates

            # Check if the file_name already exists in the list
            if file_name not in unique_files:
                unique_files.append(file_name)
                status.append([digit1])  # Append the status for the first time
                coordinates.append([coords])  # Initialize with the first set of coordinates
            else:
                # If file_name exists, add the status and coordinates
                index = unique_files.index(file_name)
                status[index].append(digit1)  # Append the status for the current line
                coordinates[index].append(coords)  # Append the coordinates for the current line

# Print the length of the arrays
print("Total unique .jpg files:", len(unique_files))
print("Unique file names:", unique_files[0])
print("Status for first file:", status[0])
print("Coordinates for first file:", coordinates[0])