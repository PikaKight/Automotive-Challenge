import os, random
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Correct path to to_send folder
PROCESSED_FOLDER = os.path.join(os.getcwd(), "Backend", "to_send")

@app.route('/get-parking-spots', methods=['POST'])
def get_parking_spots():
    # List available processed images in the folder
    processed_images = os.listdir(PROCESSED_FOLDER)  # List images

    # ✅ Debug print available images
    print(f"Available processed images: {processed_images}")

    if not processed_images:
        return jsonify({"error": "No processed images available"}), 500  # Return 500 if empty

    # Randomly select an image from the processed images folder
    selected_image = random.choice(processed_images)
    file_url = f"http://localhost:5000/processed/{selected_image}"  # Create the file URL
    print(f"File URL: {file_url}")

    # Return the file URL in the response
    return jsonify({"message": "File processed", "processed_image": file_url}), 200

@app.route('/processed/<filename>')
def serve_processed_image(filename):
    # Debug log for requested files
    print(f"Requested file: {filename}")

    # Serve the image from the 'to_send' folder
    return send_from_directory(PROCESSED_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
