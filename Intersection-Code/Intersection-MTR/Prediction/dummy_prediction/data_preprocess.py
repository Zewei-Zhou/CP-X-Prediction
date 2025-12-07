import pandas as pd
import numpy as np
import warnings
from Prediction.dummy_prediction.data_utils import *
import matplotlib.pyplot as plt
from tqdm import tqdm
import os
import pickle

# %%
object_type_subclass = {
    0: 'Other',
    1: 'Passenger_Vehicle',
    2: 'Vehicle_Other',
    3: 'VRU_Child',
    4: 'VRU_Adult',
    5: 'VRU_Adult_Using_Motorized_Bicycle',
    6: 'VRU_Adult_Using_Manual_Wheelchair',
    7: 'VRU_Adult_Using_Motorized_Wheelchair',
    8: 'VRU_Adult_Using_Cane',
    9: 'VRU_Adult_Using_Stroller',
    10: 'VRU_Adult_Using_Walker',
    11: 'VRU_Adult_Using_Manual_Bicycle',
    12: 'VRU_Adult_Using_Electric_Scooter',
    13: 'VRU_Adult_Using_Manual_Scooter',
    14: 'VRU_Adult_Using_Skateboard',
    15: 'VRU_Adult_Using_Crutches',
    16: 'VRU_Adult_Using_Cardboard_Box',
    17: 'VRU_Adult_Using_Umbrella',
    18: 'VRU_Other',
    19: 'VRU_Child_Dummy',
    20: 'VRU_Adult_Dummy',
    21: 'VRU_Adult_Using_Motorized_Bicycle_Dummy'
}

object_type_class = {
    0: 'Other',
    1: 'Vehicle',
    2: 'VRU',
    3: 'Dummy'
}
subclass_values = list(object_type_subclass.values())

pedestrian_class = ['VRU_Child', 'VRU_Adult', 'VRU_Child_Dummy', 'VRU_Adult_Dummy', 'VRU_Adult_Using_Manual_Wheelchair',\
                    'VRU_Adult_Using_Motorized_Wheelchair', 'VRU_Adult_Using_Cane', 'VRU_Adult_Using_Stroller',\
                    'VRU_Adult_Using_Walker', 'VRU_Adult_Using_Skateboard', 'VRU_Adult_Using_Crutches',
                    'VRU_Adult_Using_Cardboard_Box', '', 'VRU_Adult_Using_Umbrella']
cyclist_class = ['VRU_Adult_Using_Motorized_Bicycle','VRU_Adult_Using_Manual_Bicycle', 'VRU_Adult_Using_Motorized_Bicycle_Dummy', \
                 'VRU_Adult_Using_Electric_Scooter', 'VRU_Adult_Using_Manual_Scooter']
vehicle_class = ['Passenger_Vehicle', 'Vehicle_Other']

# final class
final_subclass = {
    0: 'VRU_Other',
    1: 'Passenger_Vehicle',
    2: 'Vehicle_Other',
    3: 'VRU_Child',
    4: 'VRU_Adult',
    5: 'VRU_Adult_Using_Wheelchair',
    6: 'VRU_Adult_Using_Bicycle',
    7: 'VRU_Adult_Using_Non-Motorized_Device/Prop_Other',
    8: 'VRU_Adult_Using_Scooter_or_Skateboard'
}

final_pedestrian_class = ['VRU_Child', 'VRU_Adult', 'VRU_Child_Dummy', 'VRU_Adult_Dummy',
                          'VRU_Adult_Using_Wheelchair',
                          'VRU_Adult_Using_Non-Motorized_Device/Prop_Other', 'VRU_Other']
final_cyclist_class = ['VRU_Adult_Using_Bicycle',
                       'VRU_Adult_Using_Bicycle_Dummy',
                       'VRU_Adult_Using_Scooter_or_Skateboard']
final_vehicle_class = ['Passenger_Vehicle', 'Vehicle_Other']

# for argoverse
challenge_to_argoverse_class = {'vehicle': ['Passenger_Vehicle'],
                                'cyclist': ['VRU_Adult_Using_Motorized_Bicycle',
                                            'VRU_Adult_Using_Electric_Scooter',
                                            'VRU_Adult_Using_Manual_Scooter',
                                            'VRU_Adult_Using_Motorized_Bicycle_Dummy']}

argoverse_class = ['vehicle', 'pedestrian', 'motorcyclist', 'cyclist', 'bus', 'static', 'background',
                         'construction', 'riderless_bicycle', 'unknown']

# scenario check information
dummy_pos_dict = None
track_heading = None


# get traj info from csv
def decode_tracks_from_csv(df,
                           object_id_start,
                           csv_file,
                           run_id,
                           subclass_mode='final',
                           use_prior_dummy_heading=True):
    global dummy_pos_dict, track_heading
    csv_keygroup = get_object_keygroups(df)
    track_infos = {
        'object_id': [],
        'object_type_subclass': [],
        'object_type_class': [],
        'trajs': []
    }

    if subclass_mode == 'final':
        object_type_subclass = final_subclass

    for key, group in csv_keygroup.items():  # retrieve each object
        # skip vehicle other
        if 'Vehicle_Other' in key:
            continue

        # get the state of the object at each timestamp
        # make sure key in order and key exists
        assert 'xctr' in group[0]
        assert 'yctr' in group[1]
        assert 'zctr' in group[2]
        assert 'xlen' in group[3]
        assert 'ylen' in group[4]
        assert 'zlen' in group[5]
        assert 'xrot' in group[6]
        assert 'yrot' in group[7]
        assert 'zrot' in group[8]

        xctr = df[group[0]].values
        yctr = df[group[1]].values
        zctr = df[group[2]].values
        xlen = df[group[3]].values
        ylen = df[group[4]].values
        zlen = df[group[5]].values
        zrot = df[group[8]].values

        # create valid token that is 1 when the vehicle has xyz value
        valid = np.ones(xctr.shape)
        valid[np.isnan(xctr) | np.isnan(yctr) | np.isnan(zctr)] = 0

        cur_subclass = '_'.join(key.split('_')[:-1])

        # get the type of the object for static and smoothing threshold and parameters
        temp_type = 'Vehicle'
        if cur_subclass in pedestrian_class:
            temp_type = 'Pedestrian'
        elif cur_subclass in cyclist_class:
            temp_type = 'Cyclist'

        if temp_type == 'Vehicle':
            static_threshold = 0.1
            k1 = 0.0001
            k2 = 0.0001
            k3 = 10
            points_per_segment = 20

        elif temp_type == 'Pedestrian':
            static_threshold = 0.015
            k1 = 0.0001
            k2 = 0.0001
            k3 = 1
            points_per_segment = 40

        elif temp_type == 'Cyclist':
            static_threshold = 0.015
            k1 = 0.0001
            k2 = 0.0001
            k3 = 1
            points_per_segment = 40

        # filter out the static points
        valid_x = xctr[valid == 1]
        valid_y = yctr[valid == 1]
        dx = np.diff(valid_x)
        dy = np.diff(valid_y)
        static_mask = (np.abs(dx) <= static_threshold) & (np.abs(dy) <= static_threshold)
        static_start = static_mask[0]
        static_mask = np.concatenate(([static_start], static_mask))

        # Create a mask for non-static parts (static_mask is not True)
        non_static_mask = ~static_mask
        # Filter out the non-static points
        non_static_x = valid_x[non_static_mask]
        non_static_y = valid_y[non_static_mask]

        # optimize the non-static points
        optimized_result = optimize_traj(non_static_x, non_static_y, k1, k2, k3, points_per_segment)

        # optimization failed since non-static points are less than (8? need to check)
        if optimized_result is None:
            print('Optimization failed')
            print(csv_file)
            print(key)

            plt.scatter(valid_x[static_mask], valid_y[static_mask], color='blue', label='Static Points')
            plt.scatter(valid_x[non_static_mask], valid_y[non_static_mask], color='orange', label='Non-static Points')
            print("-------skip this one--------")
            continue

        else:
            x_coeff_list, y_coeff_list, closest_x_points, closest_y_points, derivative_x, derivative_y = optimized_result

            optimized_valid_x = np.full(valid_x.shape, np.nan)
            optimized_valid_y = np.full(valid_y.shape, np.nan)
            optimized_valid_x[non_static_mask] = closest_x_points
            optimized_valid_y[non_static_mask] = closest_y_points

            valid_heading = np.full(valid_x.shape, np.nan)
            valid_heading[non_static_mask] = np.arctan2(derivative_y, derivative_x)

            # Fill in the static points (traj and heading), optimized_valid_x, optimized_valid_y unused now, might be deleted later
            static_indices = np.where(static_mask)[0]
            for i in static_indices:
                if i > 0:
                    # Find the last non-static point before the current static point
                    previous_non_static = i - 1
                    while previous_non_static >= 0 and static_mask[previous_non_static]:
                        previous_non_static -= 1
                    if previous_non_static >= 0:
                        optimized_valid_x[i] = optimized_valid_x[previous_non_static]
                        optimized_valid_y[i] = optimized_valid_y[previous_non_static]
                        valid_heading[i] = valid_heading[previous_non_static]

                if np.isnan(optimized_valid_x[i]):  # If no previous non-static point was found
                    # Use the next non-static point if the static point is at the start or no previous found
                    next_non_static = i + 1
                    while next_non_static < len(static_mask) and static_mask[next_non_static]:
                        next_non_static += 1
                    if next_non_static < len(static_mask):
                        optimized_valid_x[i] = optimized_valid_x[next_non_static]
                        optimized_valid_y[i] = optimized_valid_y[next_non_static]
                        valid_heading[i] = valid_heading[next_non_static]

        # get dummy heading based on the scenario check results
        if use_prior_dummy_heading and 'Dummy' in key:
            valid_heading, dummy_pos_dict, track_heading = \
                get_prior_dummy_heading(run_id, valid_heading, dummy_pos_dict, track_heading)

        # Calculate velocity
        time_disp = 0.1
        velocity_x_valid = np.zeros(len(valid_x))
        velocity_y_valid = np.zeros(len(valid_y))

        # Compute velocities for all points except the first
        velocity_x_valid[1:] = optimized_valid_x[1:] - optimized_valid_x[:-1]
        velocity_y_valid[1:] = optimized_valid_y[1:] - optimized_valid_y[:-1]

        # Assign the velocity of the second point to the first point
        velocity_x_valid[0] = velocity_x_valid[1]
        velocity_y_valid[0] = velocity_y_valid[1]

        velocity_x_valid = velocity_x_valid / time_disp
        velocity_y_valid = velocity_y_valid / time_disp

        velocity_x = np.zeros(len(xctr))
        velocity_y = np.zeros(len(yctr))
        velocity_x[valid == 1] = velocity_x_valid
        velocity_y[valid == 1] = velocity_y_valid

        headings = np.zeros(len(xctr))
        headings[valid == 1] = valid_heading

        cur_traj = np.stack([xctr, yctr, zctr,
                             xlen, ylen, zlen,
                             headings, velocity_x, velocity_y, valid], axis=1)  # (num_timestamp, 10)

        # set object_id
        track_infos['object_id'].append(object_id_start)
        object_id_start += 1
        # Passenger_Vehicle_xctr

        # set object_type_class
        if 'Dummy' in key:
            track_infos['object_type_class'].append('Dummy')
        elif 'Vehicle' in key:
            track_infos['object_type_class'].append('Vehicle')
        elif 'VRU' in key:
            track_infos['object_type_class'].append('VRU')
        else:
            track_infos['object_type_class'].append('Other')
            warnings.warn(
                f"Warning: The key '{key}' does not contain 'Dummy', 'Vehicle' or 'VRU'. Classified as 'Other'.")

        # set object_type_subclass
        cur_subclass = '_'.join(key.split('_')[:-1])

        if any(subclass in cur_subclass for subclass in subclass_values[1:]):
            track_infos['object_type_subclass'].append(cur_subclass)
        else:
            track_infos['object_type_subclass'].append('Other')
            warnings.warn(
                f"Warning: The key '{key}' does not contain any of the predefined subclass. Classified as 'Other'.")

        track_infos['trajs'].append(cur_traj)

    track_infos['trajs'] = np.stack(track_infos['trajs'], axis=0)  # (num_objects, num_timestamp, 10)
    return track_infos, object_id_start


# %%
def create_info_single_waymo_prediction_scenario(info, total_track_infos, start_timestamp,
                                                 prediction_scenario_length=91, num_historical_steps=10):
    prediction_info = {}
    prediction_info['scenario_id'] = info['file_id'] + '_' + str(start_timestamp)
    prediction_info['timestamps_seconds'] = info['timestamps_seconds'][
                                            start_timestamp: start_timestamp + prediction_scenario_length]
    # hard code current tine index
    prediction_info['current_time_index'] = num_historical_steps

    # a track is considered "track_to_predict" is it is not invalid over the whole prediction interval
    track_valid = total_track_infos['trajs'][:, start_timestamp: start_timestamp + prediction_scenario_length, -1]
    track_valid_mask = np.all(track_valid != 0, axis=1)
    track_valid_indices = np.where(track_valid_mask)[0]

    if len(track_valid_indices) == 0:
        return None

    # note that track index is consistent in the same run file, but start from 0 in each file
    prediction_info['tracks_to_predict'] = {'track_index': track_valid_indices}

    prediction_info['tracks_to_predict']['object_type_subclass'] = [total_track_infos['object_type_subclass'][cur_idx]
                                                                    for cur_idx in
                                                                    prediction_info['tracks_to_predict']['track_index']]
    prediction_info['tracks_to_predict']['object_type_class'] = [total_track_infos['object_type_class'][cur_idx] for
                                                                 cur_idx in
                                                                 prediction_info['tracks_to_predict']['track_index']]

    prediction_info['trajs'] = total_track_infos['trajs'][:,
                               start_timestamp: start_timestamp + prediction_scenario_length, :]

    prediction_info['object_id'] = total_track_infos['object_id']
    prediction_info['object_type_subclass'] = total_track_infos['object_type_subclass']
    prediction_info['object_type_class'] = total_track_infos['object_type_class']
    return prediction_info


def create_info_single_argo2_prediction_scenario(info,
                                                 total_track_infos,
                                                 start_timestamp,
                                                 prediction_scenario_length,
                                                 num_historical_steps):
    scenario_id = info['file_id'] + '_' + str(start_timestamp)
    timestamps_seconds = info['timestamps_seconds'][start_timestamp: start_timestamp + prediction_scenario_length]

    # a track is considered "track_to_predict" is it is not invalid over the whole prediction interval
    track_valid = total_track_infos['trajs'][:, start_timestamp: start_timestamp + prediction_scenario_length, -1]
    track_valid_mask = np.all(track_valid != 0, axis=1)
    track_valid_indices = np.where(track_valid_mask)[0]

    # ar least one object exists in this prediction scenario
    if len(track_valid_indices) == 0:
        return None

    object_type_subclass = total_track_infos['object_type_subclass']
    object_type_class = total_track_infos['object_type_class']

    # ----------------------------------------------------------------
    dim = 3  # hard coding
    num_agents = len(track_valid_indices)
    valid_mask = np.zeros((num_agents, prediction_scenario_length), dtype=bool)
    current_valid_mask = np.zeros(num_agents, dtype=bool)
    predict_mask = np.zeros((num_agents, prediction_scenario_length), dtype=bool)
    agent_id = [total_track_infos['object_id'][index] for index in track_valid_indices]
    agent_type = np.zeros(num_agents, dtype=int)
    agent_category = np.zeros(num_agents, dtype=int)
    position = np.zeros((num_agents, prediction_scenario_length, dim))
    heading = np.zeros((num_agents, prediction_scenario_length))
    velocity = np.zeros((num_agents, prediction_scenario_length, dim))

    # trajectories = total_track_infos['trajs'][
    #                track_valid_indices, start_timestamp: start_timestamp + prediction_scenario_length, :]
    # agent_id = total_track_infos['object_id'][track_valid_indices]

    count = 0
    for track_valid_index in track_valid_indices:
        agent_category[count] = 3  # hard coding
        trajectory = total_track_infos['trajs'][
                     track_valid_index, start_timestamp: start_timestamp + prediction_scenario_length, :]
        valid_mask[count, :] = trajectory[:, -1].astype(bool)

        # a time step t is valid only when both t and t-1 are valid
        valid_mask[count, 1: num_historical_steps] = (
                valid_mask[count, :num_historical_steps - 1] &
                valid_mask[count, 1: num_historical_steps])
        valid_mask[count, 0] = False

        current_valid_mask[count] = valid_mask[count, num_historical_steps - 1]
        if current_valid_mask[count]:
            predict_mask[count, num_historical_steps:] = valid_mask[count, num_historical_steps:]

        for class_candidate, subclass_candidates in challenge_to_argoverse_class.items():
            agent_type_temp = class_candidate \
                if object_type_subclass[count] in subclass_candidates else 'pedestrian'
            agent_type[count] = argoverse_class.index(agent_type_temp)

        position[count, :, :2] = trajectory[:, :2]
        heading[count, :] = trajectory[:, 6]
        velocity[count, :, :2] = trajectory[:, 7:9]
        count += 1

    #todo: check predition mask

    return {
        'scenario_id': scenario_id,
        'num_nodes': num_agents,
        'valid_mask': valid_mask,
        'predict_mask': predict_mask,
        'id': agent_id,
        'type': agent_type,
        'category': agent_category,
        'position': position,
        'heading': heading,
        'velocity': velocity,
    }

def get_prior_dummy_heading(run_id, valid_heading,
                            dummy_pos_dict, track_heading):
    # hard coding the path
    if not dummy_pos_dict:
        combined_dict = np.load('/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/combined_dict.npy', allow_pickle=True).item()
        dummy_pos_dict = {}
        for direction, details in combined_dict['dummy_heading_dict'].items():
            for run in details['run']:
                dummy_pos_dict[run] = direction

    if not track_heading:
        with open('/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/track_heading.pkl', 'rb') as f:
            track_heading = pickle.load(f)

    if int(run_id) in dummy_pos_dict:
        track_pos = dummy_pos_dict[int(run_id)].split('_')[0]
        track_direction = dummy_pos_dict[int(run_id)].split('_')[-1]
        heading = track_heading[int(track_pos)][int(track_direction)]
        valid_heading[:] = heading

    return valid_heading, dummy_pos_dict, track_heading


# %%
def create_infos_from_csv(csv_file, object_id_start):
    df = pd.read_csv(csv_file)
    csv_keygroup = get_object_keygroups(df)
    info = {}
    info['file_id'] = csv_file.split('/')[-1].split('_')[1]
    if 'Time' in df:
        info['timestamps_seconds'] = list(df['Time'])
    else:
        info['timestamps_seconds'] = list(df['frame_id'])
    info['prediction_scenarios'] = []
    total_track_infos, object_id_start = decode_tracks_from_csv(df, object_id_start, csv_file, info['file_id'])

    # prediction_scenario_length = 110  # past 49, current 1, future 60 hard coding
    num_historical_steps = 50
    prediction_scenario_length = 51 # past 50, current 1, future 50

    # todo: cut off
    timestamp_cut_off = int((len(info['timestamps_seconds']) - prediction_scenario_length) * 0.75)

    for start_timestamp in range(len(info['timestamps_seconds']) - prediction_scenario_length):
        # todo: cut off
        if start_timestamp == timestamp_cut_off:

            prediction_info = create_info_single_waymo_prediction_scenario(info, total_track_infos, start_timestamp,
                                                                           prediction_scenario_length, num_historical_steps)
            # prediction_info = create_info_single_argo2_prediction_scenario(info, total_track_infos, start_timestamp,
            #                                                                prediction_scenario_length, num_historical_steps)
            if prediction_info is None:
                continue

            info['prediction_scenarios'].append(prediction_info)
    info['object_type_class'] = total_track_infos['object_type_class']
    info['object_type_subclass'] = total_track_infos['object_type_subclass']
    info['trajs'] = total_track_infos['trajs']
    return info, object_id_start

if __name__ == "__main__":
    # loop all the scenarios
    # root_dirs = ['/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation',
    #             '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation2',
    #              '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation3',
    #             '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/validation_GT_second_release']
    # root_dirs = ['/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/validation_GT_second_release']
    root_dirs = ['/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/rehearsal_3/group_a']
    # '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation3',
    for index, root_dir in enumerate(root_dirs):
        if index == 0:
            csv_files = []
        csv_files += sorted([os.path.join(root_dir, x)
                             for x in os.listdir(root_dir) if
                             x.endswith('.csv')])
    info_all = {}
    object_id_start = 0
    for csv_file in csv_files:
        info, object_id_start = create_infos_from_csv(csv_file, object_id_start)
        info_all.update({info['file_id']: info})

    output_path = './processed_scenarios'
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f'info_reh_a.pkl')
    with open(output_file, 'wb') as f:
        pickle.dump(info_all, f)