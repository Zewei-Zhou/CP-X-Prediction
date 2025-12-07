import os
import csv

source_folder = "/Users/zewei/01_Projects/202405_Safety_challenge/validation_GT_second_release"
target_folder = "/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/validation_GT_second_release"

for file_name in os.listdir(source_folder):
    if file_name.endswith(".csv"):
        source_file_path = os.path.join(source_folder, file_name)
        target_file_name = file_name.replace(".csv", "_GT.csv")
        target_file_path = os.path.join(target_folder, target_file_name)

        if os.path.exists(target_file_path):
            with open(source_file_path, 'r') as source_file:
                source_reader = csv.reader(source_file)
                source_header = next(source_reader)
                timestamps = [row[0] for row in source_reader]

            with open(target_file_path, 'r') as target_file:
                target_reader = csv.reader(target_file)
                target_data = list(target_reader)

            target_header = target_data[0]
            for i, row in enumerate(target_data[1:], start=0):
                row[0] = timestamps[i]

            with open(target_file_path, 'w', newline='') as target_file:
                target_writer = csv.writer(target_file)
                target_writer.writerow(target_header)
                target_writer.writerows(target_data[1:])
        else:
            print(f"{target_file_name} not found in the target folder.")
