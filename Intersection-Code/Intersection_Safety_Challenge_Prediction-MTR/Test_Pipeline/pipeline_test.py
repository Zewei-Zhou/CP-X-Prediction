import glob
import pandas as pd
import torch
import io
import imageio
import numpy as np
from tqdm import tqdm
from model import MTR
from matplotlib import pyplot as plt
from train_utils import batch_nms
from test_utils import *
from data_process import *
from conflict import calculate_conflict

# Data
prefix = "./test_data/group_*"
all_files = glob.glob(f'{prefix}/*.csv')

# Build model
model_checkpoint = './epoch=42.ckpt'
device = torch.device('cuda')
model = MTR.load_from_checkpoint(model_checkpoint, map_location=device)
model.eval()

# Build map
with open('vector_map.pkl', 'rb') as file:
    vector_map = pickle.load(file)

# Load the dummy heading from the scenario check
combined_dict = np.load('./combined_dict.npy', allow_pickle=True).item()
dummy_pos_dict = {}
for direction, details in combined_dict['dummy_heading_dict'].items():
    for run in details['run']:
        dummy_pos_dict[run] = direction

# Load the prior offline track heading
with open('./track_heading.pkl', 'rb') as f:
    track_heading = pickle.load(f)

# Parameters
output_path = 'results_output'
os.makedirs(output_path, exist_ok=True)
history_timesteps = 30
interval = 10
save_vis = False


# Functions
def process_from_df(scenario_id, df, vector_map):
    traj_info = {}
    csv_keygroup = get_object_keygroups(df)

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

        if np.sum(valid) > 20:
            s_traj = smooth_trajectory(traj[valid == 1], window_length=21, order=3)
        else:
            s_traj = traj[valid == 1]

        traj[valid == 1] = s_traj
        heading = calculate_heading(traj) if 'Dummy' not in key \
            else get_prior_dummy_heading(scenario_id, traj,
                                         dummy_pos_dict, track_heading)
        velocity = calculate_velocity(traj)
        traj[-2:] = raw_traj[-2:]
        traj = np.concatenate([traj, heading[:, None], velocity], axis=-1)

        # raw trajectory
        traj_info[key.replace('_xctr', '')] = {'traj': traj, 'sub_class': subclass, 'valid': valid,
                                               'x_len': x_len, 'y_len': y_len, 'z_len': z_len, 'zctr': zctr}

    map_info = decode_map_features_from_proto(vector_map.map_features)

    return traj_info, map_info


def process_model_input(center_agent, center_idx, trajectory_data, map_data, debug=False):
    center_object_state = center_agent['traj'][-1]
    object_trajs = np.stack([v['traj'][-history_timesteps:] for k, v in trajectory_data.items()], axis=0)
    objects, map_polyline = transform_to_center_frame(center_object_state, object_trajs, map_data)

    # put center object at the first index in order
    order = list(range(objects.shape[0]))
    order[0], order[center_idx] = order[center_idx], order[0]

    # fill in array
    hist_trajs = np.zeros((5, history_timesteps, 6), dtype=np.float32)  # x, y, heading, v_x, v_y, type
    hist_valid = np.zeros((5, history_timesteps), dtype=np.float32)

    for i, idx in enumerate(order):
        if i >= objects.shape[0]:
            break

        traj = objects[idx]
        valid = trajectory_data[list(trajectory_data.keys())[idx]]['valid'][-history_timesteps:]
        sub_class = trajectory_data[list(trajectory_data.keys())[idx]]['sub_class']

        if 'Device' in sub_class:
            sub_class = 'VRU_Adult_Using_Non-Motorized_Device/Prop_Other'

        type = class_values.index(sub_class)

        hist_trajs[i, :, :5] = traj
        hist_trajs[i, :, 5] = type
        hist_valid[i, :] = valid

    inputs = {'hist_trajs': hist_trajs, 'hist_valid': hist_valid, 'maps': map_polyline}

    if debug:
        plt.figure(figsize=(10, 10))
        for k in range(map_polyline.shape[0]):
            plt.plot(map_polyline[k, :, 0], map_polyline[k, :, 1], 'k--', linewidth=2)

        for k in range(objects.shape[0]):
            plt.scatter(objects[k, :, 0], objects[k, :, 1], s=100, label='Agent %d' % k)

        plt.axis('equal')
        plt.show()

    return inputs


def filter_invalid_predictions(sub_class, prediction_trajs, prediction_scores, map):
    map_points = map.copy().reshape(-1, map.shape[-1])
    raw_prediction_scores = prediction_scores.copy()

    if 'Vehicle' in sub_class:
        for i in range(prediction_trajs.shape[0]):
            if check_vehicle_off_road(prediction_trajs[i], map_points):
                raw_prediction_scores[i] = 0.0

    else:
        for i in range(prediction_trajs.shape[0]):
            if check_vru_off_area(prediction_trajs[i], map_points):
                raw_prediction_scores[i] = 0.0

    if np.sum(raw_prediction_scores) == 0:
        pass
    else:
        prediction_trajs = np.delete(prediction_trajs, np.where(raw_prediction_scores == 0.0), axis=0)
        prediction_scores = np.delete(prediction_scores, np.where(raw_prediction_scores == 0.0), axis=0)
        prediction_scores = prediction_scores / np.sum(prediction_scores)

    return prediction_trajs, prediction_scores


def check_vehicle_off_road(traj, map):
    road = map[map[..., 3] == 1]

    for i in range(traj.shape[0]):
        dist = np.linalg.norm(traj[i] - road[:, :2], axis=1)
        min_dist = np.min(dist)
        if min_dist > 4.0:
            return True

    return False


def check_vru_off_area(traj, map):
    sidewalk = map[map[..., 3] == 2]
    crosswalk = map[map[..., 3] == 3]
    area = np.concatenate([sidewalk, crosswalk], axis=0)

    for i in range(traj.shape[0]):
        dist = np.linalg.norm(traj[i] - area[:, :2], axis=1)
        min_dist = np.min(dist)
        if min_dist > 4.0:
            return True

    return False


## Begin testing pipeline
conflict_prediction = pd.DataFrame()
metric_ade_df = pd.DataFrame()

# Iterate over all GT data
for file in tqdm(test_files):
    data = pd.read_csv(file)
    scenario_id = file.split('/')[-1].split('.')[0].replace('_GT', '')
    tqdm.write(f'Processing scenario {scenario_id}')
    timestamps = data['Time']
    conflict_pred = []
    figs = []

    # Iterate over all timestamps
    for j, t in enumerate(timestamps):
        # Skip start and end of scenario
        if j < 100 or j >= len(timestamps) - 100:
            continue

        # Skip interval
        if j % interval != 0:
            continue

        # get trajectory data, map data, and future GT data
        raw_perception_data = data.iloc[:j]
        future_timesteps = timestamps[j:j + 50]
        trajectory_data, map_data = process_from_df(scenario_id,
                                                    raw_perception_data,
                                                    vector_map)

        # Iterate over all valid agents
        path_prediction_results = {}

        for ki, k in enumerate(trajectory_data.keys()):
            agent_trajectory_data = trajectory_data[k]

            # skip if not enough history data
            if agent_trajectory_data['valid'][-1] == 0:
                continue

            # get model prediction (replace with your model)
            inputs = process_model_input(agent_trajectory_data, ki, trajectory_data, map_data)
            inputs = {k: torch.tensor(v).unsqueeze(0).to(device) for k, v in inputs.items()}
            outputs = model(inputs)

            prediction_trajs = outputs['layer_3_trajs'].detach().cpu()
            prediction_scores = outputs['layer_3_scores'].detach().cpu().softmax(dim=1)
            prediction_trajs = prediction_trajs[0].numpy()
            prediction_scores = prediction_scores[0].numpy()

            # to global frame
            center_state = agent_trajectory_data['traj'][-1]
            global_prediction_trajs = transformer_to_global_frame(prediction_trajs, center_state)

            # filter invalid predictions
            global_prediction_trajs, prediction_scores = filter_invalid_predictions(k, global_prediction_trajs,
                                                                                    prediction_scores, map_data)
            path_prediction_results[k] = (global_prediction_trajs, prediction_scores)

        # plot results and save gif
        plt.figure(figsize=(10, 10))
        plot_vector_map()

        colors = ['r', 'g', 'b', 'c', 'm']
        for a_i, a in enumerate(path_prediction_results.keys()):
            plot_agent(trajectory_data[a]['traj'][-1], trajectory_data[a]['sub_class'], color=colors[a_i])
            plot_trajectory(path_prediction_results[a][0], color=colors[a_i])

        plt.title(f'Scenario {scenario_id}, Time {t}')
        plt.xlim(-40, 60)
        plt.ylim(-50, 40)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        figs.append(imageio.v2.imread(buf))
        plt.close()
                
        # save path prediction results in csv
        prediction_df = pd.DataFrame()

        # iterate over future timesteps
        for dt, c_t in enumerate(future_timesteps):
            # iterate over all agents
            for ki, k in enumerate(trajectory_data.keys()):
                if k not in path_prediction_results:
                    result = {'Timestamps': c_t, 'ID': k, 'path_ID': 1, 'subclass': trajectory_data[k]['sub_class'],
                              'x_center': np.nan, 'y_center': np.nan, 'z_center': np.nan, 'x_length': np.nan,
                              'y_length': np.nan, 'z_length': np.nan, 'confidence_score': np.nan}
                    # prediction_df = pd.concat([prediction_df, pd.DataFrame(result, index=[0])], axis=0)

                else:  # iterate over all paths
                    for p in range(path_prediction_results[k][0].shape[0]):
                        pred_pos = path_prediction_results[k][0][p][dt]
                        pred_score = path_prediction_results[k][1][p]
                        sub_class = trajectory_data[k]['sub_class'].replace('_Dummy', '')
                        result = {'Timestamps': c_t, 'ID': k, 'path_ID': p + 1, 'subclass': sub_class,
                                  'x_center': pred_pos[0], 'y_center': pred_pos[1],
                                  'z_center': trajectory_data[k]['zctr'],
                                  'x_length': trajectory_data[k]['x_len'], 'y_length': trajectory_data[k]['y_len'],
                                  'z_length': trajectory_data[k]['z_len'], 'confidence_score': pred_score}
                        prediction_df = pd.concat([prediction_df, pd.DataFrame(result, index=[0])], axis=0)

        # save results
        # use path_id to reorganize the dataframe
        if not prediction_df.empty:
            prediction_df = prediction_df.sort_values(by=['ID', 'path_ID'])
            prediction_df.to_csv(f'{output_path}/{scenario_id}_{timestamp}_Path_Prediction_Submission_File.csv',
                                 index=False)

        # conflict prediction
        objects = {k: (trajectory_data[k]['sub_class'].replace('_Dummy', ''),
                       (trajectory_data[k]['y_len'], trajectory_data[k]['x_len']))
                   for k in path_prediction_results.keys()}
        conflict, ttc, ru1_subclass, ru2_subclass = calculate_conflict(path_prediction_results, objects)
        conflict_timestamp = t + ttc if conflict else None
        conflict_pred.append((conflict, conflict_timestamp, ru1_subclass, ru2_subclass))

    # Save visualization as gif
    if save_vis:
        imageio.mimsave(f'./{scenario_id}.gif', figs, duration=0.1 * interval)

        # Save conflict prediction results
    min_ttc = np.inf
    ru1_subclass = np.nan
    ru2_subclass = np.nan
    if conflict:
        for c in conflict_pred:
            if c[0] and c[1] < min_ttc:
                min_ttc = c[1]
                ru1_subclass = c[2]
                ru2_subclass = c[3]

    result = {'Run ID': scenario_id, 'Conflict_No_Conflict_Label': 'conflict' if conflict else 'no conflict',
              'timestamp_conflict': np.nan if not conflict else min_ttc,
              'road_user1_subclass': ru1_subclass, 'road_user2_subclass': ru2_subclass}
    conflict_prediction = pd.concat([conflict_prediction, pd.DataFrame(result, index=[0])], axis=0)


# save results
conflict_prediction.to_csv('./Conflict_Prediction_Submission_File.csv', index=False)
