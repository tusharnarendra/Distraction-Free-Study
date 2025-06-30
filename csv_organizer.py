import os
import csv

dataset_root = 'dataset' 
output_csv = 'results.csv'

class_folders = ['focused', 'studying', 'distracted']

failed_detections = set() 

class_labels = {
    'focused': 0,
    'studying': 1,
    'distracted': 2
}

with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['image_name', 'focused/studying/distracted'])

    count = 0

    for folder_name in class_folders:
        folder_path = os.path.join(dataset_root, folder_name)
        if not os.path.isdir(folder_path):
            print(f"Warning: Folder not found: {folder_path}")
            continue
        image_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith('.jpg')])

        for image_file in image_files:
            image_name = f"{image_file}"

            if image_name in failed_detections:
                count += 1
                continue

            classification_value = class_labels.get(folder_name, -1)

            writer.writerow([image_name, classification_value])
            count += 1

print(f"Finished processing {count} images (written + skipped).")
