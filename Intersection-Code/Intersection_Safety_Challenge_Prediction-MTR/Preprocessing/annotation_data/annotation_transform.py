import os
import json
import pandas as pd
import numpy as np
import csv
from collections import defaultdict
from datetime import datetime

# Time format
time_format = "%Y-%m-%d-%H-%M-%S_%f"


def read_json_files(base_dir):
    scenes_data = {}

    for scene in os.listdir(base_dir):

        scene_path = os.path.join(base_dir, scene)

        if os.path.isdir(scene_path):
            lidar_new_path = os.path.join(scene_path, 'label')

            # todo: just for testing
            # if float(scene) != 91:
            #     continue

            if os.path.isdir(lidar_new_path):
                scenes_data[scene] = {}

                json_files = sorted([f for f in os.listdir(lidar_new_path) if f.endswith('.json')])

                for json_file in json_files:
                    json_file_path = os.path.join(lidar_new_path, json_file)

                    with open(json_file_path, 'r') as file:
                        data = json.load(file)

                        timestamp = json_file.split('.')[0]

                        for obj in data:
                            if 'obj_id' in obj:
                                obj_id = obj['obj_id']
                            else:
                                raise ValueError(f"No object id in {json_file}.")

                            obj_type = obj.get('obj_type', None)
                            obj_attr = obj.get('obj_attr', None)
                            psr = obj.get('psr', None)

                            # filter the Unknown and static vehicle object
                            if obj_type == 'Unknown' or obj_type == 'Vehicle_Other':
                                continue

                            if obj_id not in scenes_data[scene]:
                                scenes_data[scene][obj_id] = {
                                    'timestamps': [timestamp],
                                    'psrs': [psr],
                                    'obj_type': obj_type,
                                    'obj_attr': obj_attr
                                }
                            else:
                                scenes_data[scene][obj_id]['timestamps'].append(timestamp)
                                scenes_data[scene][obj_id]['psrs'].append(psr)

    return scenes_data


def annotation_to_challenge(base_dir):
    scenes_data = read_json_files(base_dir)

    # Initialize a dictionary to store columns for each scene
    scene_columns = {}

    for scene_id, scene in scenes_data.items():
        data_storage = defaultdict(list)
        # todo: revise the run 390
        if scene_id == '390':
            timestamps = scene['8']['timestamps']
        else:
            timestamps = scene[next(iter(scene))]['timestamps']
        obj_type_dict = {}  # assumption: object 1 is always in those scenarios

        for obj_id, obj_content in scene.items():
            obj_type = obj_content['obj_type']

            # filter the static objects
            if obj_type in ['Misc', 'Traffic_Signal_Pole', 'Tree']:
                continue

            if obj_content['obj_attr'] == 'dummy':
                obj_type += '_Dummy'

            if "Moterized" in obj_type:
                obj_type = obj_type.replace("Moterized", "Motorized")

            for i, timestamp in enumerate(obj_content['timestamps']):
                psr = obj_content['psrs'][i]

                # coordination transformation
                x = psr['position']['y']
                y = - psr['position']['x']
                x_len = psr['scale']['y']
                y_len = psr['scale']['x']

                if -50 <= x <= 80 and -70 <= y <= 75:
                    data_storage[timestamp].append({
                        'obj_type': obj_type,
                        'obj_id': obj_id,
                        'xctr': x,
                        'yctr': y,
                        'zctr': psr['position']['z'],
                        'xlen': x_len,
                        'ylen': y_len,
                        'zlen': psr['scale']['z'],
                        'xrot': psr['rotation']['x'],
                        'yrot': psr['rotation']['y'],
                        'zrot': psr['rotation']['z']
                    })

                    if obj_id not in obj_type_dict:
                        obj_type_dict[obj_id] = obj_type

                    if timestamp not in scene_columns:
                        scene_columns[timestamp] = set()
                    scene_columns[timestamp].add(obj_type)

        output_file = os.path.join(base_dir, f"Run_{scene_id}_GT.csv")

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Generate the header
            header = ['Time']
            for obj_id, obj_type in obj_type_dict.items():
                header.extend([f"{obj_type}_xctr", f"{obj_type}_yctr", f"{obj_type}_zctr",
                               f"{obj_type}_xlen", f"{obj_type}_ylen", f"{obj_type}_zlen",
                               f"{obj_type}_xrot", f"{obj_type}_yrot", f"{obj_type}_zrot"])
            writer.writerow(header)

            obj_id_list = list(obj_type_dict.keys())
            for timestamp in timestamps:
                # timestamp to unix timestamp
                dt = datetime.strptime(timestamp, time_format)
                unix_timestamp = dt.timestamp()

                row = [str(unix_timestamp)] + [None] * (len(obj_type_dict) * 9)
                if timestamp in data_storage:
                    for entry in data_storage[timestamp]:
                        position = obj_id_list.index(entry['obj_id'])
                        base_index = position * 9 + 1
                        row[base_index:base_index + 9] = [
                            entry['xctr'], entry['yctr'], entry['zctr'], entry['xlen'], entry['ylen'], entry['zlen'],
                            entry['xrot'], entry['yrot'], entry['zrot']
                        ]
                writer.writerow(row)

    return scenes_data


################################################################
base_dirs = ['/Volumes/safety_challenge_annotation_data2/lidar_annotation_third']

# from annotation format to challenge format
# The annotation have a lot of errors, and need further manual process
for base_dir in base_dirs:
    annotation_to_challenge(base_dir)
