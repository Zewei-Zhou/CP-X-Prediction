import os
import numpy as np
import csv
import matplotlib.pyplot as plt
from Prediction.dummy_prediction.data_preprocess import create_infos_from_csv


def read_detection_data_txt(root_folder):
    object_trajectories = {}

    for run_folder in os.listdir(root_folder):
        run_folder_path = os.path.join(root_folder, run_folder)
        if os.path.isdir(run_folder_path) and run_folder.startswith('run'):
            run_number = run_folder.split('run')[1]
            object_trajectories[run_number] = {}
            filename = os.path.join(run_folder_path, f'{run_number}_connected_trajectories.txt')
            if os.path.isfile(filename):
                with open(filename, 'r') as file:
                    for line in file:
                        parts = line.strip().split(',')
                        frame = int(float(parts[0]))
                        obj_id = int(float(parts[1]))
                        center_x = float(parts[3])
                        center_y = -float(parts[2])
                        center_z = float(parts[4])
                        if obj_id not in object_trajectories[run_number]:
                            object_trajectories[run_number][obj_id] = {'x': [], 'y': []}
                        object_trajectories[run_number][obj_id]['x'].append(center_x)
                        object_trajectories[run_number][obj_id]['y'].append(center_y)
    return object_trajectories


def read_detection_data_csv(root_folder):
    object_trajectories = {}

    for file in os.listdir(root_folder):
        file_path = os.path.join(root_folder, file)
        if os.path.isfile(file_path) and file.endswith('.csv'):
            run_number = file.split('.')[0]  # Assuming the filename is like 'run1.csv', 'run2.csv', etc.
            object_trajectories[run_number] = {}
            with open(file_path, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                next(csvreader)  # Skip the header row
                for row in csvreader:
                    frame = int(float(row[0]))
                    obj_id = int(float(row[1]))
                    center_x = float(row[3])
                    center_y = -float(row[2])
                    center_z = float(row[4])
                    if obj_id not in object_trajectories[run_number]:
                        object_trajectories[run_number][obj_id] = {'x': [], 'y': []}
                    object_trajectories[run_number][obj_id]['x'].append(center_x)
                    object_trajectories[run_number][obj_id]['y'].append(center_y)

    return object_trajectories


def read_gt_data(root_dir):
    csv_files = sorted([os.path.join(root_dir, x) for x in os.listdir(root_dir) if x.endswith('.csv')])
    info_all = {}
    for csv_file in csv_files:
        info, object_id_start = create_infos_from_csv(csv_file)
        info_all.update({info['file_id']: info})
    return info_all


def plot_trajectories(detection_trajectories, gt_data):
    for run_number, trajectories in detection_trajectories.items():
        plt.figure(figsize=(10, 8))
        for obj_id, trajectory in trajectories.items():
            plt.plot(trajectory['x'], trajectory['y'], label=f'Detected Object {obj_id}')

        trajs = gt_data[run_number]['trajs']
        for i in range(trajs.shape[0]):
            object_type_subclass = gt_data[run_number]['object_type_subclass'][i]
            valid_trajs = np.array([trajs[i, j, :2] for j in range(trajs.shape[1]) if trajs[i, j, -1] > 0])
            plt.plot(valid_trajs[:, 0], valid_trajs[:, 1],
                     linewidth=2.5, alpha=.9, linestyle='--', color='gray',
                     label=object_type_subclass if object_type_subclass not in plt.gca().get_legend_handles_labels()[
                         1] else "")
            plt.plot(valid_trajs[0, 0], valid_trajs[0, 1], marker='*', markersize=10)

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(f'Object Trajectories Over Time in run{run_number}')
        plt.legend()
        plt.show()


detection_outputs_dir = '/Preprocessing/detection_results/detection_outputs'
gt_root_dir = '/Users/zewei/01_Projects/202405_Safety_challenge/validation_GT_second_release'

# detection_trajectories = read_detection_data_txt(detection_outputs_dir)
detection_trajectories = read_detection_data_csv(detection_outputs_dir)


gt_data = read_gt_data(gt_root_dir)

plot_trajectories(detection_trajectories, gt_data)
