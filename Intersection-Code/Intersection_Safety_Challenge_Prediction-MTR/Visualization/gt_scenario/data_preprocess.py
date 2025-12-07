import pandas as pd
import numpy as np
import warnings
import os
import matplotlib.pyplot as plt
import uuid
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
from scipy.optimize import dual_annealing

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


# for argoverse
challenge_to_argoverse_class = {'vehicle': ['Passenger_Vehicle'],
                                'cyclist': ['VRU_Adult_Using_Motorized_Bicycle',
                                            'VRU_Adult_Using_Electric_Scooter',
                                            'VRU_Adult_Using_Manual_Scooter',
                                            'VRU_Adult_Using_Motorized_Bicycle_Dummy']}

argoverse_class = ['vehicle', 'pedestrian', 'motorcyclist', 'cyclist', 'bus', 'static', 'background',
                         'construction', 'riderless_bicycle', 'unknown']


def get_object_keygroups(df):
    # Group columns based on each item
    groups = {}
    current_group = []
    current_key = 'Timestamp'
    # Print the column names to help identify the timestamp columns
    for col in df.columns:
        if 'xctr' in col:  # Assuming each group starts with 'xctr'
            if current_group:
                groups[current_key] = current_group

            current_key = col
            current_group = [col]
        else:
            current_group.append(col)

    # Add the last group
    if current_group:
        groups[current_key] = current_group

    groups.pop('Timestamp')
    return groups

#
def decode_tracks_from_csv(df, object_id_start):
    csv_keygroup = get_object_keygroups(df)
    track_infos = {
        'object_id': [],
        'object_type_subclass': [],
        'object_type_class': [],
        'trajs': []
    }

    for key, group in csv_keygroup.items():  # retrieve each object
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

        # calculate velocity
        # xctr_disp = np.diff(xctr, prepend=xctr[0])
        # yctr_disp = np.diff(yctr, prepend=yctr[0])

        def calculate_disp_and_heading(xctr, yctr, valid):
            disp_x = []
            disp_y = []
            headings = []

            # process the first element
            dx, dy, heading_temp = 0, 0, None
            if valid[0] == 1 and valid[1] == 1:
                # if x0 != nan, x1 != nan, then v0 = x1 - x0
                dx = xctr[1] - xctr[0]
                dy = yctr[1] - yctr[0]
                heading_temp = np.arctan2(dy, dx)
            disp_x.append(dx)
            disp_y.append(dy)
            headings.append(heading_temp)

            for i in range(1, len(xctr)):
                if valid[i] == 0:
                    # not valid, displacement set to 0
                    dx, dy, heading_temp = 0, 0, None
                else:
                    # if x i-1 is not valid, set vi = xi+1 - xi (i.e. vi = vi+1)
                    if valid[i - 1] == 0:
                        # if xi+1 is valid, then vi = xi+1 - xi
                        if i < len(xctr) - 1 and valid[i + 1] != 0:
                            dx = xctr[i + 1] - xctr[i]
                            dy = yctr[i + 1] - yctr[i]
                            heading_temp = np.arctan2(dy, dx)
                        # is xi+1 is not valid, then vi = 0 (i don't think this will happen)
                        else:
                            dx, dy, heading_temp = 0, 0, None
                    else:
                        # common case: xi-1 and xi are both valid, vi = xi - xi-1
                        dx = xctr[i] - xctr[i - 1]
                        dy = yctr[i] - yctr[i - 1]
                        heading_temp = np.arctan2(dy, dx)
                disp_x.append(dx)
                disp_y.append(dy)
                headings.append(heading_temp)
            return np.array(disp_x), np.array(disp_y), np.array(headings)

        time_disp = 0.1  # 10 Hz, hardcode rn
        xctr_disp, yctr_disp, headings = calculate_disp_and_heading(xctr, yctr, valid)
        xctr_velocity = xctr_disp / time_disp
        yctr_velocity = yctr_disp / time_disp

        # zrot from 0-360 degree to [-pi, pi]

        # assert np.all((zrot[~np.isnan(zrot)] >= 0) & (zrot[~np.isnan(zrot)] <= 360))
        # zrot_radians = np.full_like(zrot, np.nan, dtype=np.float64)
        # zrot_non_nan_mask = ~np.isnan(zrot)
        # zrot_non_nan = zrot[zrot_non_nan_mask]
        # zrot_radians[zrot_non_nan_mask] = np.deg2rad(zrot_non_nan)
        # zrot_radians[zrot_non_nan_mask] = (zrot_radians[zrot_non_nan_mask] + np.pi) % (2 * np.pi) - np.pi
        zrot_radians = headings

        # todo: fill the 0 heading with the other heading

        cur_traj = np.stack([xctr, yctr, zctr,
                             xlen, ylen, zlen,
                             zrot_radians, xctr_velocity,
                             yctr_velocity, valid],
                            axis=1)  # (num_timestamp, 10)

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

    track_infos['trajs'] = np.stack(track_infos['trajs'], axis=0)  # (num_objects, num_timestamp, 9)
    return track_infos, object_id_start


# %%
def create_info_single_waymo_prediction_scenario(info, total_track_infos, start_timestamp,
                                                 prediction_scenario_length=91):
    prediction_info = {}
    prediction_info['scenario_id'] = info['file_id'] + '_' + str(start_timestamp)
    prediction_info['timestamps_seconds'] = info['timestamps_seconds'][
                                            start_timestamp: start_timestamp + prediction_scenario_length]
    # hard code current tine index
    prediction_info['current_time_index'] = 10

    # a track is considered "track_to_predict" is it is not invalid over the whole prediction interval
    track_valid = total_track_infos['trajs'][:, start_timestamp: start_timestamp + prediction_scenario_length, -1]
    track_valid_mask = np.all(track_valid != 0, axis=1)
    track_valid_indices = np.where(track_valid_mask)[0]

    if len(track_valid_indices) == 0:
        return None

    # note that track index is consistent in the same run file, but start from 0 in each file
    prediction_info['tracks_to_predict'] = {
        'track_index': track_valid_indices
    }

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
    total_track_infos, object_id_start = decode_tracks_from_csv(df, object_id_start)

    # prediction_scenario_length = 110  # past 49, current 1, future 60 hard coding
    # num_historical_steps = 50
    prediction_scenario_length = 91
    for start_timestamp in range(len(info['timestamps_seconds']) - prediction_scenario_length + 1):
        prediction_info = create_info_single_waymo_prediction_scenario(info, total_track_infos, start_timestamp,
                                                                       prediction_scenario_length)
        # prediction_info = create_info_single_argo2_prediction_scenario(info, total_track_infos, start_timestamp,
        #                                                                prediction_scenario_length, num_historical_steps)
        if prediction_info is None:
            continue

        info['prediction_scenarios'].append(prediction_info)
    info['object_type_class'] = total_track_infos['object_type_class']
    info['object_type_subclass'] = total_track_infos['object_type_subclass']
    info['trajs'] = total_track_infos['trajs']
    return info, object_id_start