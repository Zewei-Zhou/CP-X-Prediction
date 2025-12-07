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

        def calculate_disp(ctr):
            disp = []
            if valid[0] == 1:
                # if x0 != nan, x1 != nan, then v0 = x1 - x0
                if valid[1] == 1:
                    disp.append(ctr[1] - ctr[0])
                # if x0 != nan and x1 = nan, then v0 = 0
                else:
                    disp.append(0)
            else:
                disp.append(0)
            for i in range(1, len(ctr)):
                if valid[i] == 0:
                    # not valid, displacement set to 0
                    disp.append(0)
                else:
                    # if x i-1 is not valid, set vi = xi+1 - xi (i.e. vi = vi+1)
                    if valid[i - 1] == 0:
                        # if xi+1 is valid, then vi = xi+1 - xi
                        if i < len(ctr) - 1 and valid[i + 1] != 0:
                            disp.append(ctr[i + 1] - ctr[i])
                        # is xi+1 is not valid, then vi = 0 (i don't think this will happen)
                        else:
                            disp.append(0)
                    else:
                        # common case: xi-1 and xi are both valid, vi = xi - xi-1
                        disp.append(ctr[i] - ctr[i - 1])
            return np.array(disp)

        time_disp = 0.1  # 10 Hz, hardcode rn
        xctr_velocity = calculate_disp(xctr) / time_disp
        yctr_velocity = calculate_disp(yctr) / time_disp

        # zrot from 0-360 degree to [-pi, pi]

        # assert np.all((zrot[~np.isnan(zrot)] >= 0) & (zrot[~np.isnan(zrot)] <= 360))
        zrot_radians = np.full_like(zrot, np.nan, dtype=np.float64)
        zrot_non_nan_mask = ~np.isnan(zrot)
        zrot_non_nan = zrot[zrot_non_nan_mask]
        zrot_radians[zrot_non_nan_mask] = np.deg2rad(zrot_non_nan)
        zrot_radians[zrot_non_nan_mask] = (zrot_radians[zrot_non_nan_mask] + np.pi) % (2 * np.pi) - np.pi

        cur_traj = np.stack([xctr, yctr, zctr, xlen, ylen, zlen, zrot_radians, xctr_velocity, yctr_velocity, valid],
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


def create_info_single_prediction_scenario(info, total_track_infos, start_timestamp, prediction_scenario_length=91):
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


def create_infos_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    csv_keygroup = get_object_keygroups(df)
    info = {}
    info['file_id'] = csv_file.split('/')[-1].split('_')[1]
    info['timestamps_seconds'] = list(df['Time'])
    info['prediction_scenarios'] = []
    total_track_infos, object_id_start = decode_tracks_from_csv(df, 0)

    prediction_scenario_length = 91  # past 10, current 1, future 80
    for start_timestamp in range(len(info['timestamps_seconds']) - prediction_scenario_length + 1):
        prediction_info = create_info_single_prediction_scenario(info, total_track_infos, start_timestamp,
                                                                 prediction_scenario_length)
        if prediction_info is None:
            continue

        info['prediction_scenarios'].append(prediction_info)
    info['object_type_class'] = total_track_infos['object_type_class']
    info['object_type_subclass'] = total_track_infos['object_type_subclass']
    info['trajs'] = total_track_infos['trajs']
    return info, object_id_start

# ----------------------------------------------------------------
# loop all the scenarios
# root_dir = '/Users/zewei/01_Projects/202405_Safety_challenge/validation_GT'
# root_dir = '/Users/zewei/01_Projects/202405_Safety_challenge/validation_GT_second_release'
# csv_files = sorted([os.path.join(root_dir, x)
#                     for x in os.listdir(root_dir) if
#                     x.endswith('.csv')])
#
# info_all = {}
# for csv_file in csv_files:
#     info, object_id_start = create_infos_from_csv(csv_file)
#     info_all.update({info['file_id']: info})
