import os
import random

folder_to_clean = "/data/dataset/CP-X-Prediction/Waymo/validation_processed"

percent_to_delete = 70  # Percentage of files to delete
files = [f for f in os.listdir(folder_to_clean) if f.endswith(".pkl")]
number_of_files = len(files)
randomized_files = random.sample(files, int(percent_to_delete * number_of_files)//(100))
for file_path in randomized_files:
    try:
        os.remove(os.path.join(folder_to_clean, file_path))
        print(f"Deleted: {file_path}")
    except OSError as e:
        print(f"Error deleting {file_path}: {e}")