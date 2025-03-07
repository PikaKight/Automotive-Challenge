import os
import cv2
import yaml
from ultralytics import YOLO

# --------------------- USER-DEFINED PATHS ---------------------
TRAIN_IMAGES_DIR = "train_images"
VAL_IMAGES_DIR   = "val_images"
TRAIN_LABELS_TXT = "train_labels.txt"
VAL_LABELS_TXT   = "val_labels.txt"

# --------------------- CLASS MAPPING --------------------------
# According to your readme:
#  - class_id = 1 -> empty
#  - class_id = 2 -> occupied
# We'll map them to YOLO classes:
#  0 -> empty
#  1 -> occupied
CLASS_MAPPING = {
    1: 0,  # empty
    2: 1   # occupied
}

# YOLO class names in index order
CLASS_NAMES = ["empty", "occupied"]

def convert_to_yolo_txt(labels_file, images_dir, output_labels_dir):
    """
    Reads a label file (train_labels.txt or val_labels.txt) with lines in the format:
      image_file class_id x_min x_max y_min y_max

    Creates YOLO annotation files in the same format YOLO expects:
      class x_center_norm y_center_norm width_norm height_norm

    Args:
        labels_file (str): Path to the labels text file.
        images_dir (str): Directory containing the corresponding images.
        output_labels_dir (str): Directory where YOLO .txt files will be written.
    """
    if not os.path.exists(output_labels_dir):
        os.makedirs(output_labels_dir, exist_ok=True)

    # Dictionary to accumulate lines per image: { image_name -> [list of YOLO lines] }
    yolo_data = {}
    num_lines_processed = 0
    num_images_found = 0

    with open(labels_file, 'r') as f:
        print(f"Reading labels from: {labels_file}")
        for line in f:
            # The readme says each line is:
            # image_file class_id x_min x_max y_min y_max
            parts = line.strip().split()
            if len(parts) != 6:
                continue  # Skip malformed lines

            img_name, cls_str, x_min_str, x_max_str, y_min_str, y_max_str = parts
            cls_id = int(cls_str)
            x_min, x_max = float(x_min_str), float(x_max_str)
            y_min, y_max = float(y_min_str), float(y_max_str)

            # Build the full path to the image
            img_path = os.path.join(images_dir, img_name)
            if not os.path.exists(img_path):
                # If the image file doesn't exist, skip
                continue

            # Read image to get dimensions
            img = cv2.imread(img_path)
            if img is None:
                continue
            height, width = img.shape[:2]
            num_images_found += 1

            # Ensure bounding box is within the image boundaries
            x_min = max(0, min(x_min, width - 1))
            x_max = max(0, min(x_max, width - 1))
            y_min = max(0, min(y_min, height - 1))
            y_max = max(0, min(y_max, height - 1))

            # Check if bounding box is valid
            if x_max <= x_min or y_max <= y_min:
                continue

            # Convert the class ID to YOLO's index
            if cls_id not in CLASS_MAPPING:
                # Unknown label; skip or handle differently
                continue
            yolo_cls_id = CLASS_MAPPING[cls_id]

            # YOLO expects normalized coords: (x_center, y_center, w, h)
            bbox_width  = x_max - x_min
            bbox_height = y_max - y_min
            x_center = x_min + bbox_width / 2.0
            y_center = y_min + bbox_height / 2.0

            x_center_norm = x_center / width
            y_center_norm = y_center / height
            w_norm        = bbox_width / width
            h_norm        = bbox_height / height

            # Create the line for YOLO
            line_yolo = f"{yolo_cls_id} {x_center_norm:.6f} {y_center_norm:.6f} {w_norm:.6f} {h_norm:.6f}"

            if img_name not in yolo_data:
                yolo_data[img_name] = []
            yolo_data[img_name].append(line_yolo)
            num_lines_processed += 1

    # Write out .txt files for each image
    for img_name, lines in yolo_data.items():
        # Remove extension from image filename
        base_name, _ = os.path.splitext(img_name)
        txt_name = base_name + ".txt"
        txt_path = os.path.join(output_labels_dir, txt_name)

        with open(txt_path, 'w') as f_txt:
            for line_yolo in lines:
                f_txt.write(line_yolo + "\n")

    print(f"Finished converting {num_lines_processed} bounding boxes for {labels_file}.")
    print(f"Annotation files saved in: {output_labels_dir}")
    print(f"Total images processed from {labels_file}: {len(yolo_data.keys())} (Found {num_images_found} images).")
    print("---------------------------------------------------\n")

def prepare_dataset():
    """
    Prepares the YOLO-compatible folder structure by:
      1) Converting bounding boxes to YOLO format
      2) Creating a 'parking_data.yaml' file that specifies dataset paths and classes.
    """
    print("===== Step 1: Converting dataset to YOLO format =====")
    # Convert train labels
    convert_to_yolo_txt(TRAIN_LABELS_TXT, TRAIN_IMAGES_DIR, TRAIN_IMAGES_DIR)
    # Convert val labels
    convert_to_yolo_txt(VAL_LABELS_TXT, VAL_IMAGES_DIR, VAL_IMAGES_DIR)

    # Create data.yaml for YOLO
    data_yaml = {
        'train': os.path.abspath(TRAIN_IMAGES_DIR),
        'val':   os.path.abspath(VAL_IMAGES_DIR),
        'nc': len(CLASS_NAMES),          # number of classes
        'names': CLASS_NAMES             # list of class names
    }

    with open('parking_data.yaml', 'w') as f:
        yaml.dump(data_yaml, f)

    print("Created 'parking_data.yaml' for YOLO training.")
    print("===== Dataset preparation completed. =====\n")

def train_yolo():
    """
    Train a YOLOv8 model (from Ultralytics) on the parking dataset.
    The training results (weights, etc.) are saved to runs/detect/<exp_name>.
    """
    print("===== Step 2: Starting YOLO training =====")
    # Start from a small pretrained model (yolov8n.pt)
    model = YOLO("yolov8n.pt")

    # Train
    print("Training in progress... This may take a while depending on your hardware.")
    results = model.train(
        data="parking_data.yaml",
        epochs=10,          # Increase for better results
        imgsz=640,          # Image size
        batch=4,            # Adjust based on GPU memory
        name="parking_yolo" # Experiment name
    )

    print("Training complete. Results saved to:", results.project)
    print("===== YOLO training finished. =====\n")

def validate_yolo():
    """
    Validate the trained YOLO model on the validation set.
    This computes mAP, precision, recall, etc.
    """
    print("===== Step 3: Validating the YOLO model =====")
    best_model_path = "runs/detect/parking_yolo/weights/best.pt"
    if not os.path.exists(best_model_path):
        print("Best model not found. Make sure training has completed.")
        return

    model = YOLO(best_model_path)
    print("Running validation on the validation set...")
    val_results = model.val()

    # val_results.metrics is a dictionary containing the metrics
    # Common keys: 'precision', 'recall', 'map50', 'map'
    metrics = val_results.metrics
    precision = metrics.get('precision', 0.0)
    recall    = metrics.get('recall', 0.0)
    map50     = metrics.get('map50', 0.0)  # AP at IoU=50
    map50_95  = metrics.get('map', 0.0)    # AP at IoU=50:95

    print(f"Validation Metrics:\n"
          f"  Precision: {precision:.4f}\n"
          f"  Recall:    {recall:.4f}\n"
          f"  mAP@0.50:  {map50:.4f}\n"
          f"  mAP@0.50:0.95: {map50_95:.4f}")
    print("===== Validation completed. =====\n")

def predict_on_image(image_path):
    """
    Runs inference on a single image and displays the bounding boxes for 'empty' vs 'occupied'.
    The best model from training is used for prediction.
    """
    print(f"===== Step 4: Running inference on image: {image_path} =====")
    best_model_path = "runs/detect/parking_yolo/weights/best.pt"
    if not os.path.exists(best_model_path):
        print("Best model not found. Please train first.")
        return

    model = YOLO(best_model_path)
    print("Performing prediction...")
    results = model.predict(source=image_path, conf=0.25)  # Adjust confidence threshold as needed

    if len(results) == 0:
        print("No detection results for:", image_path)
        return

    # Retrieve detections
    dets = results[0].boxes.boxes.cpu().numpy()  # shape: (num_detections, 6)
    img = cv2.imread(image_path)
    if img is None:
        print("Could not load image:", image_path)
        return

    print(f"Found {dets.shape[0]} bounding boxes in the image.")
    for *bbox, conf, cls_id in dets:
        x1, y1, x2, y2 = map(int, bbox)
        cls_id = int(cls_id)
        label_str = CLASS_NAMES[cls_id]

        # Color-coded bounding box: green for empty, red for occupied
        color = (0, 255, 0) if label_str == "empty" else (0, 0, 255)

        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            img,
            f"{label_str} {conf:.2f}",
            (x1, max(0, y1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )

    # Display the image with drawn bounding boxes
    cv2.imshow("YOLO Inference", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    print("===== Inference complete. Check the displayed image window. =====\n")

def main():
    # 1) Prepare the dataset: convert bounding boxes & create parking_data.yaml
    prepare_dataset()

    # 2) Train the YOLO model
    train_yolo()

    # 3) Validate (outputs mAP, precision, recall, etc.)
    validate_yolo()

    # 4) Run inference on a sample validation image (replace with an actual file)
    sample_val_image = os.path.join(VAL_IMAGES_DIR, "2012-09-11_15_29_29.jpg")
    if os.path.exists(sample_val_image):
        predict_on_image(sample_val_image)
    else:
        print("Sample validation image not found for inference demo.")

if __name__ == "__main__":
    main()