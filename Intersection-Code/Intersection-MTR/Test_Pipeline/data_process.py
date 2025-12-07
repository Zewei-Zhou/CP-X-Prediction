import glob
import os
import pandas as pd
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
from test_utils import *
from data_utils import *


# Data
prefix = "/home/zhiyu/Projects/Project13/Intersection_Safety_Challenge_Prediction/Data/perception_results" #validation_GT_second_release
traj_val_gt_files = glob.glob(os.path.join(prefix, "*.csv"))
val_files = [f'{prefix}/Run_179_GT.csv', f'{prefix}/Run_315_GT.csv', 
            f'{prefix}/Run_214_GT.csv', f'{prefix}/Run_410_GT.csv', 
            f'{prefix}/Run_1078_GT.csv', f'{prefix}/Run_91_GT.csv', 
            f'{prefix}/Run_875_GT.csv', f'{prefix}/Run_448_GT.csv',
            f'{prefix}/Run_363_GT.csv', f'{prefix}/Run_48_GT.csv']
train_files = list(set(traj_val_gt_files) - set(val_files))

# Object class
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
    18: 'VRU_Adult_Dummy',
    19: 'VRU_Child_Dummy',
    20: 'VRU_Adult_Using_Motorized_Bicycle_Dummy',
    21: 'VRU_Other',
}

object_type_class = {
    0: 'Other',
    1: 'Vehicle',
    2: 'VRU'
}
subclass_values = list(object_type_subclass.values())

pedestrian_class = ['VRU_Child', 'VRU_Adult', 'VRU_Child_Dummy', 'VRU_Adult_Dummy', 'VRU_Adult_Using_Manual_Wheelchair',\
                    'VRU_Adult_Using_Motorized_Wheelchair', 'VRU_Adult_Using_Cane', 'VRU_Adult_Using_Stroller',\
                    'VRU_Adult_Using_Walker', 'VRU_Adult_Using_Skateboard', 'VRU_Adult_Using_Crutches', 
                    'VRU_Adult_Using_Cardboard_Box', '', 'VRU_Adult_Using_Umbrella']
cyclist_class = ['VRU_Adult_Using_Motorized_Bicycle','VRU_Adult_Using_Manual_Bicycle', 'VRU_Adult_Using_Motorized_Bicycle_Dummy', \
                 'VRU_Adult_Using_Electric_Scooter', 'VRU_Adult_Using_Manual_Scooter']
vehicle_class = ['Passenger_Vehicle', 'Vehicle_Other']


# map class
map_class = {
    0: 'Other',
    1: 'Lane',
    2: 'SideWalk',
    3: 'CrossWalk',
    4: 'Boundary',
}

# Build map
with open('/home/tianhui/Intersection_Safety_Challenge_Prediction/map/vector_map.pkl', 'rb') as file:
    vector_map = pickle.load(file)

# Parameters
output_path = 'data_process_output/train_perception'
os.makedirs(output_path, exist_ok=True)
history_timesteps = 11
future_timesteps = 80
interval = 2


# Functions
def process_from_df(df, vector_map):
    traj_info = {}
    csv_keygroup = get_object_keygroups(df)

    for key, group in csv_keygroup.items(): # retrieve each object
        # skip vehicle other
        if 'Vehicle_Other' in key:
            continue
        
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

        # valid mask
        valid = np.ones(xctr.shape)
        valid[np.isnan(xctr) | np.isnan(yctr) | np.isnan(zctr)] = 0

        # get the sub_class of the object
        subclass = '_'.join(key.split('_')[:-1])
        
        # get trajectory
        traj = np.stack([xctr, yctr], axis=-1)
        if np.any(valid == 0) and valid[-1] == 1:
            traj = interpolate_trajectory(traj)
            valid[np.isfinite(traj[:, 0])] = 1
        
        traj = np.nan_to_num(traj, nan=0.0)    
        x_len = xlen[-1] if not np.isnan(xlen[-1]) else 0.0
        y_len = ylen[-1] if not np.isnan(ylen[-1]) else 0.0
        z_len = zlen[-1] if not np.isnan(zlen[-1]) else 0.0
        zctr = zctr[-1] if not np.isnan(zctr[-1]) else 0.0

        if np.sum(valid) > history_timesteps:
            s_traj = smooth_trajectory(traj[valid==1], window_length=11)
        else:
            s_traj = traj[valid==1]

        traj[valid==1] = s_traj
        heading = calculate_heading(traj)
        velocity = calculate_velocity(traj)
        traj = np.concatenate([traj, heading[:, None], velocity], axis=-1)
        
        # raw trajectory
        traj_info[key.replace('_xctr', '')] = {'traj': traj, 'sub_class': subclass, 'valid': valid, 
                                               'x_len': x_len, 'y_len': y_len, 'z_len': z_len, 'zctr': zctr}

    map_info = decode_map_features_from_proto(vector_map.map_features)
  
    return traj_info, map_info

def process_gt_from_df(df):
    gt = {}
    csv_keygroup = get_object_keygroups(df)

    for key, group in csv_keygroup.items(): # retrieve each object
        # skip vehicle other
        if 'Vehicle_Other' in key:
            continue

        xctr = df[group[0]].values
        yctr = df[group[1]].values
        zctr = df[group[2]].values
        xlen = df[group[3]].values
        ylen = df[group[4]].values
        zlen = df[group[5]].values

        # valid mask
        valid = np.ones(xctr.shape)
        valid[np.isnan(xctr) | np.isnan(yctr) | np.isnan(zctr)] = 0

        # get trajectory
        traj = np.stack([xctr, yctr], axis=-1)
        if np.any(valid == 0) and valid[0] == 1:
            traj = interpolate_trajectory(traj)
            valid[np.isfinite(traj[:, 0])] = 1

        traj = np.nan_to_num(traj, nan=0.0)

        if np.all(valid[:20] == 1): # require at least 20 frames to be valid
            s_traj = smooth_trajectory(traj[valid==1], window_length=19)
            traj[valid==1] = s_traj
        else:
            traj = np.zeros_like(traj)
            valid = np.zeros_like(valid)            
        
        # smooth raw trajectory
        gt[key.replace('_xctr', '')] = {'traj': traj, 'valid': valid}
  
    return gt

def process_model_input(trajectory_data, center_idx, map_data, future_data, debug=False):
    center_object_state = trajectory_data[list(trajectory_data.keys())[center_idx]]['traj'][-1]
    object_trajs = np.stack([v['traj'][-history_timesteps:] for k, v in trajectory_data.items()], axis=0)
    objects, map_polyline = transform_to_center_frame(center_object_state, object_trajs, map_data)
    future_trajs = np.stack([v['traj'] for k, v in future_data.items()], axis=0)
    objects_future = transform_to_center_frame_no_rotation(center_object_state, future_trajs)

     # put center object at the first index in order
    order = list(range(objects.shape[0]))
    order[0], order[center_idx] = order[center_idx], order[0]

    # fill in array
    hist_trajs = np.zeros((5, history_timesteps, 6), dtype=np.float32) # x, y, heading, v_x, v_y, type
    hist_valid = np.zeros((5, history_timesteps), dtype=np.float32)
    fut_trajs = np.zeros((5, future_timesteps, 2), dtype=np.float32)
    fut_valid = np.zeros((5, future_timesteps), dtype=np.float32)
 
    for i, idx in enumerate(order):
        if i >= len(trajectory_data):
            break

        traj = objects[idx]
        valid = trajectory_data[list(trajectory_data.keys())[idx]]['valid'][-history_timesteps:]
        sub_class = trajectory_data[list(trajectory_data.keys())[idx]]['sub_class']
        type = subclass_values.index(sub_class)
        hist_trajs[i, :, :5] = traj
        hist_trajs[i, :, 5] = type
        hist_valid[i, :] = valid

        future_traj = objects_future[idx]
        valid = future_data[list(future_data.keys())[idx]]['valid']
        fut_trajs[i, :, :] = future_traj
        fut_valid[i, :] = valid
    
    inputs = {'hist_trajs': hist_trajs, 'maps': map_polyline, 'fut_gt_trajs': fut_trajs,
              'hist_valid': hist_valid, 'fut_valid': fut_valid}
    
    if debug:
        plt.figure(figsize=(10, 10))
        for k in range(map_polyline.shape[0]):
            plt.plot(map_polyline[k, :, 0], map_polyline[k, :, 1], 'k--', linewidth=2)
  
        for k in range(hist_trajs.shape[0]):
            plt.scatter(hist_trajs[k, :, 0], hist_trajs[k, :, 1], s=100, label='Agent %d' % k)
        
        for k in range(fut_trajs.shape[0]):
            plt.plot(fut_trajs[k, :, 0], fut_trajs[k, :, 1], 'r--', linewidth=2)
          
        plt.axis('equal')
        plt.show()
    
    return inputs


if __name__ == '__main__':
    # Process data
    for i in tqdm(range(len(train_files))):
        raw_data = pd.read_csv(train_files[i])
        scenario_id = train_files[i].split('/')[-1].split('.')[0].replace('_GT', '')
        tqdm.write(f'Processing scenario {scenario_id}')
        timestamps = raw_data['Time']
        conflict_pred = []
        
        # Iterate over all timestamps
        for j, t in enumerate(timestamps):
            # skip start and end of scenario
            if j < 100 or j > len(timestamps) - 100:
                continue

            # skip some frames
            if j % interval != 0:
                continue

            # get trajectory data, map data, and future GT data
            raw_perception_data = raw_data.iloc[:j+1]
            trajectory_data, map_data = process_from_df(raw_perception_data, vector_map)
            future_gt_data = process_gt_from_df(raw_data.iloc[j+1:j+81])

            # for each agent as center
            for ki, k in enumerate(trajectory_data.keys()):
                agent_trajectory_data = trajectory_data[k]

                # require all history timesteps to be valid
                if np.sum(agent_trajectory_data['valid'][-history_timesteps:]) < history_timesteps:
                    continue
                
                # process model input
                inputs = process_model_input(trajectory_data, ki, map_data, future_gt_data)

                # save data
                with open(f'{output_path}/{scenario_id}_{t}_{k}.pkl', 'wb') as file:
                    pickle.dump(inputs, file)

                # add more data for vehicle 
                if agent_trajectory_data['sub_class'] in vehicle_class:
                    for d in range(5):
                        inputs = process_model_input(trajectory_data, ki, map_data, future_gt_data)
                        with open(f'{output_path}/{scenario_id}_{t}_{k}_{d+1}.pkl', 'wb') as file:
                            pickle.dump(inputs, file)