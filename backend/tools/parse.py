def parse_lines(file_path):
    parsed_data = {}
    
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            key = parts[0]
            values = list(map(float, parts[1:]))  # Convert numbers to float
            
            if key in parsed_data:
                parsed_data[key].append(values)
            else:
                parsed_data[key] = [values]
    
    return parsed_data

if __name__ == "__main__":
# Example usage
    file_path = r"C:\Users\aaqil\Downloads\parking_dataset\train_labels.txt"  # Replace with your actual file path
    data = parse_lines(file_path)