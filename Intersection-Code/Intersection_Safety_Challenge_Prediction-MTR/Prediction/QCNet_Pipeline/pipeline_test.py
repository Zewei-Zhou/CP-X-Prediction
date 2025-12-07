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
prefix = "/home/zhiyu/Projects/Project13/Intersection_Safety_Challenge_Prediction/Data/validation_GT_second_release" 
all_files = glob.glob(f'{prefix}/*.csv')
conflict_labels = pd.read_csv('conflict_no_conflict_labels_all_validation_runs.csv')
test_files = [f'{prefix}/Run_179_GT.csv', f'{prefix}/Run_315_GT.csv', 
            f'{prefix}/Run_214_GT.csv', f'{prefix}/Run_410_GT.csv', 
            f'{prefix}/Run_1078_GT.csv', f'{prefix}/Run_91_GT.csv', 
            f'{prefix}/Run_875_GT.csv', f'{prefix}/Run_448_GT.csv',
            f'{prefix}/Run_363_GT.csv', f'{prefix}/Run_48_GT.csv']

# Build model
model_checkpoint = '/home/zhiyu/Projects/Project13/Predictor_v3/output/perception_annotation_gt/epoch=42.ckpt'
device = torch.device('cuda')
model = MTR.load_from_checkpoint(model_checkpoint, map_location=device)
model.eval()

# Build map
with open('vector_map.pkl', 'rb') as file:
    vector_map = pickle.load(file)

# Parameters
output_path = 'results_output'
os.makedirs(output_path, exist_ok=True)
history_timesteps = 11
future_timesteps = 80
interval = 10
save_vis = False


# Functions
def process_from_df(df, vector_map):
    traj_info = {}
    csv_keygroup = get_object_keygroups(df)

    for key, group in csv_keygroup.items(): # retrieve each object
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
        traj = np.nan_to_num(traj, nan=0.0)
        
        # smooth raw trajectory
        gt[key.replace('_xctr', '')] = {'traj': traj, 'valid': valid}
  
    return gt

def process_model_input(center_agent, center_idx, trajectory_data, map_data, debug=False):
    center_object_state = center_agent['traj'][-1]
    object_trajs = np.stack([v['traj'][-history_timesteps:] for k, v in trajectory_data.items()], axis=0)
    objects, map_polyline = transform_to_center_frame(center_object_state, object_trajs, map_data)
    
    # put center object at the first index in order
    order = list(range(objects.shape[0]))
    order[0], order[center_idx] = order[center_idx], order[0]

    # fill in array
    hist_trajs = np.zeros((5, history_timesteps, 6), dtype=np.float32) # x, y, heading, v_x, v_y, type
    hist_valid = np.zeros((5, history_timesteps), dtype=np.float32)

    for i, idx in enumerate(order):
        if i >= objects.shape[0]:
            break

        traj = objects[idx]
        valid = trajectory_data[list(trajectory_data.keys())[idx]]['valid'][-history_timesteps:]
        sub_class = trajectory_data[list(trajectory_data.keys())[idx]]['sub_class']
        type = subclass_values.index(sub_class)
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
        trajectory_data, map_data = process_from_df(raw_perception_data, vector_map)
        future_gt_data = process_gt_from_df(data.iloc[j:j+future_timesteps])

        # Iterate over all valid agents
        path_prediction_results = {}

        for ki, k in enumerate(trajectory_data.keys()):
            agent_trajectory_data = trajectory_data[k]

            # skip if not enough history data
            if np.sum(agent_trajectory_data['valid'][-history_timesteps:]) < history_timesteps:
                continue

            # get model prediction (replace with your model)
            inputs = process_model_input(agent_trajectory_data, ki, trajectory_data, map_data)
            inputs = {k: torch.tensor(v).unsqueeze(0).to(device) for k, v in inputs.items()}
            outputs = model(inputs)

            prediction_trajs = outputs['layer_3_trajs'].detach().cpu()
            prediction_scores = outputs['layer_3_scores'].detach().cpu().softmax(dim=1)
            prediction_trajs = prediction_trajs[0].numpy()
            prediction_scores = prediction_scores[0].numpy()
            prediction_scores = prediction_scores / np.sum(prediction_scores)

            # to global frame
            center_state = agent_trajectory_data['traj'][-1]
            global_prediction_trajs = transformer_to_global_frame(prediction_trajs, center_state)
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
        for dt in range(future_timesteps):
            c_t = float(t) + (dt+1) * 0.1 
            for ki, k in enumerate(trajectory_data.keys()):
                for p in range(3): # three path prediction
                    if k not in path_prediction_results:
                        result = {'Time': c_t, 'path_ID': p+1, 'sub_class': trajectory_data[k]['sub_class'], 
                                  'x_center': np.nan, 'y_center': np.nan, 'z_center': np.nan, 'x_length': np.nan,
                                  'y_length': np.nan, 'z_length': np.nan, 'confidence_score': np.nan}
                        #prediction_df = pd.concat([prediction_df, pd.DataFrame(result, index=[0])], axis=0)
                    else:
                        pred_pos = path_prediction_results[k][0][p][dt]
                        pred_score = path_prediction_results[k][1][p]
                        result = {'Time': c_t, 'path_ID': p+1, 'sub_class': trajectory_data[k]['sub_class'], 
                                  'x_center': pred_pos[0], 'y_center': pred_pos[1], 'z_center': trajectory_data[k]['zctr'],
                                  'x_length': trajectory_data[k]['x_len'], 'y_length': trajectory_data[k]['y_len'], 
                                  'z_length': trajectory_data[k]['z_len'], 'confidence_score': pred_score}
                        prediction_df = pd.concat([prediction_df, pd.DataFrame(result, index=[0])], axis=0)
            
        prediction_df.to_csv(f'{output_path}/{scenario_id}_{t}.csv', index=False)

        # calculate ADE
        for ki, k in enumerate(trajectory_data.keys()):
            if k not in path_prediction_results:
                continue

            fut_trajs = future_gt_data[k]['traj']
            fut_valid = future_gt_data[k]['valid']
            prediction_trajs, prediction_scores = path_prediction_results[k]
            error = np.linalg.norm(prediction_trajs[..., :2] - fut_trajs[None, :, :], axis=-1)
            error = error * fut_valid
            weighted_error = np.sum(error * prediction_scores[:, None], axis=0)
            ade = np.sum(weighted_error) / np.sum(fut_valid) if np.sum(fut_valid) > 0 else 0.0
            result = {'scenario_id': scenario_id, 'time': t, 'object_ID': k, 'ADE': ade}
            metric_ade_df = pd.concat([metric_ade_df, pd.DataFrame(result, index=[0])], axis=0)

        # calculate conflict
        objects = {k: (trajectory_data[k]['sub_class'], (trajectory_data[k]['y_len'], trajectory_data[k]['x_len'])) 
                   for k in path_prediction_results.keys()}
        conflict, ttc, ru1_subclass, ru2_subclass = calculate_conflict(path_prediction_results, objects)
        conflict_timestamp = t + ttc if conflict else None
        conflict_pred.append((conflict, conflict_timestamp, ru1_subclass, ru2_subclass))

    # Save visualization as gif
    if save_vis:
        imageio.mimsave(f'./{scenario_id}.gif', figs, duration=0.1*interval)

    # Get ground truth conflict labels
    conflict_gt = conflict_labels[conflict_labels['Run ID'] == scenario_id]['Conflict_No_Conflict_Label'].values
    conflict = any([c[0] for c in conflict_pred])
    
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
              'timestamp_conflict': min_ttc, 'road_user1_subclass': ru1_subclass, 'road_user2_subclass': ru2_subclass}
    conflict_prediction = pd.concat([conflict_prediction, pd.DataFrame(result, index=[0])], axis=0)


# save results
metric_ade_df.to_csv('weighted_ADE_results.csv', index=False)
conflict_prediction.to_csv('conflict_prediction_results.csv', index=False)

# report results
ade_results = pd.read_csv('weighted_ADE_results.csv')
print(f'Trajectory Prediction == Total Weighted ADE: {ade_results["ADE"].mean()}')
dummy_ade_results = ade_results[ade_results['object_ID'].str.contains('Dummy')]
print(f'Trajectory Prediction == Dummy Weighted ADE: {dummy_ade_results["ADE"].mean()}')
vehicle_ade_results = ade_results[ade_results['object_ID'].str.contains('Vehicle')]
print(f'Trajectory Prediction == Vehicle Weighted ADE: {vehicle_ade_results["ADE"].mean()}')
vru_ade_results = ade_results[ade_results['object_ID'].str.contains('VRU')]
vru_ade_results = vru_ade_results[['Dummy' not in x for x in vru_ade_results['object_ID']]]
print(f'Trajectory Prediction == VRU Weighted ADE: {vru_ade_results["ADE"].mean()}')


FP, FN, TP, TN = 0, 0, 0, 0
conflict_results = pd.read_csv('conflict_prediction_results.csv')
runs = conflict_results['Run ID']
for run in runs:
    pred = conflict_results[conflict_results['Run ID'] == run]['Conflict_No_Conflict_Label'].values[0]
    gt = conflict_labels[conflict_labels['Run ID'] == run]['Conflict_No_Conflict_Label'].values[0]
    print(f'Run ID: {run}, Prediction: {pred}, Ground Truth: {gt}')
    if pred == 'conflict' and gt == 'conflict':
        TP += 1
    elif pred == 'conflict' and gt == 'no conflict':
        FP += 1
    elif pred == 'no conflict' and gt == 'conflict':
        FN += 1
    else:
        TN += 1

print(f'Conflict Prediction == FP: {FP}, FN: {FN}, TP: {TP}, TN: {TN}')
F2 = 5 * TP / (5 * TP + 4 * FN + FP + 1e-6)
print(f'Conflict Predictino == F2 score: {F2}')

