import glob
import pandas as pd
import torch
import io
import imageio
import numpy as np
from tqdm import tqdm
from matplotlib import pyplot as plt
import datetime
import matplotlib.animation as animation
from train_utils import batch_nms
from test_utils import *
from data_process import *
from conflict import calculate_conflict
from mtr.models import model as model_utils
from mtr.datasets import build_dataloader
from mtr.config import cfg, cfg_from_list, cfg_from_yaml_file, log_config_to_file
from mtr_utils import *
# Data
all_files = glob.glob("../Data/rehearsal_3/*.csv")
# GT_data = glob.glob("../Data/validation_GT_second_release/*.csv")
# all_files = ['../Data/validation_GT_second_release/Run_179_GT.csv','../Data/validation_GT_second_release/Run_315_GT.csv','../Data/validation_GT_second_release/Run_214_GT.csv','../Data/validation_GT_second_release/Run_410_GT.csv','../Data/validation_GT_second_release/Run_1078_GT.csv','../Data/validation_GT_second_release/Run_91_GT.csv','../Data/validation_GT_second_release/Run_448_GT.csv',\
#              '../Data/validation_GT_second_release/Run_875_GT.csv', '../Data/validation_GT_second_release/Run_48_GT.csv','../Data/validation_GT_second_release/Run_363_GT.csv']

conflict_labels = pd.read_csv('/home/tianhui/Intersection_Safety_Challenge_Prediction/Pipeline_New/conflict_no_conflict_labels_all_validation_runs.csv')

# load config
cfg_file = '/home/tianhui/Intersection_Safety_Challenge_Prediction/Prediction/MTR/tools/cfgs/challenge/mtr+val+ann12+p12_data_withmap_h1sf5s_cluster32_1.yaml'
cfg_from_yaml_file(cfg_file, cfg)
dataset_cfg=cfg.DATA_CONFIG


# Build model
output_dir = Path("MTR_TEST")
log_file = output_dir / ('log_loaddata_%s.txt' % datetime.datetime.now().strftime('%Y%m%d-%H%M%S'))
logger = common_utils.create_logger(log_file, rank=cfg.LOCAL_RANK)
# model_checkpoint = '../Prediction/MTR/output/challenge/mtr+val+ann12_data_withmap_h1s_cluster32/val_ann12_h1s_cluster32/ckpt/checkpoint_epoch_30.pth'
# model_checkpoint_new = '/home/tianhui/Intersection_Safety_Challenge_Prediction/Prediction/MTR/output/challenge/mtr+val+ann12+p12_data_withmap_h1s_cluster32/default/ckpt/best_model.pth'
model_checkpoint_h5s = '/home/tianhui/Intersection_Safety_Challenge_Prediction/Prediction/MTR/output/challenge/mtr+val+ann12+p12_data_withmap_h1sf5s_cluster32_1/default/ckpt/best_model.pth'
device = torch.device('cuda')
model = model_utils.MotionTransformer(config=cfg.MODEL).to(device)
model.load_params_from_file(model_checkpoint_h5s, logger=logger, to_cpu=False)
model.eval()
# Build map
with open("../map/vector_map.pkl", "rb") as f:
    vector_map = pickle.load(f)

with open('vector_map.pkl', 'rb') as file:
    map_postprocess = pickle.load(file)
    map_data_postprocess = decode_map_features_from_proto_postprocess(map_postprocess.map_features)

# Parameters
output_path = 'mtr_result_rehearsal_3'
os.makedirs(output_path, exist_ok=True)
history_timesteps = 11
interval = 40
DT = 1
save_vis = False


# Functions
def process_from_df(df, vector_map, t=None):
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
        z_ctr = zctr[-1] if not np.isnan(zctr[-1]) else 0.0

        # if np.sum(valid) > history_timesteps:
        #     s_traj = smooth_trajectory(traj[valid==1], window_length=11)
        # else:
        #     s_traj = traj[valid==1]

        # traj[valid==1] = s_traj
        # heading = calculate_heading(traj)
        if np.sum(valid) > history_timesteps:
            heading = calculate_heading_smoothed(xctr, yctr, valid, subclass)
        else:
            heading = calculate_heading(traj)

        if np.sum(valid) > history_timesteps:

            time_disp = 0.1
            valid_x = xctr[valid == 1]
            valid_y = yctr[valid == 1]
            velocity_x_valid = np.zeros(len(valid_x))
            velocity_y_valid = np.zeros(len(valid_y))

            # Compute velocities for all points except the first
            velocity_x_valid[1:] = valid_x[1:] - valid_x[:-1]
            velocity_y_valid[1:] = valid_y[1:] - valid_y[:-1]

            # Assign the velocity of the second point to the first point
            velocity_x_valid[0] = velocity_x_valid[1]
            velocity_y_valid[0] = velocity_y_valid[1]

            velocity_x_valid = velocity_x_valid/time_disp
            velocity_y_valid = velocity_y_valid/time_disp

            velocity_x = np.zeros(len(xctr))
            velocity_y = np.zeros(len(yctr))
            velocity_x[valid == 1] = velocity_x_valid
            velocity_y[valid == 1] = velocity_y_valid

        else:
            velocity = calculate_velocity(traj)
            velocity_x = velocity[:, 0]
            velocity_y = velocity[:, 1]

        traj = np.concatenate([traj, heading[:, None], velocity_x[:,None], velocity_y[:,None]], axis=-1)
        # traj_mtr = np.concatenate([xctr[:, None], yctr[:, None], zctr[:, None], xlen[:, None], ylen[:, None], zlen[:, None], heading[:, None], velocity, valid[:, None]],axis=-1)
        traj_mtr = np.concatenate([xctr[:, None], yctr[:, None], zctr[:, None], xlen[:, None], ylen[:, None], zlen[:, None], heading[:, None], velocity_x[:,None], velocity_y[:,None], valid[:, None]],axis=-1)

        if t is not None:
            traj = traj[:t,:]
            traj_mtr = traj_mtr[:t,:]
            valid = valid[:t]
        # breakpoint()
        traj_info[key.replace('_xctr', '')] = {'traj': traj, 'traj_mtr': traj_mtr, 'sub_class': subclass, 'valid': valid, 
                                               'x_len': x_len, 'y_len': y_len, 'z_len': z_len, 'zctr': z_ctr}

    map_info = decode_map_features_from_proto_mtr(vector_map.map_features)
  
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

def calculate_minADE(result):
    min_ade_list = []
    min_ade_vehicle = []
    min_ade_pedestrian = []
    min_ade_cyclist = []
    min_ade_dummy = []

    for i in range(len(result)):
        for j in range(len(result[i])):
            pred_trajs = result[i][j]['pred_trajs']
            gt_trajs = result[i][j]['gt_trajs'][11:,:2]

            # Calculate ADE for each mode
            ade_list = []
            for mode in range(pred_trajs.shape[0]):
                distance = np.sum((gt_trajs - pred_trajs[mode])**2, axis=1)
                distance = np.sqrt(distance)
                ade = np.mean(distance)
                ade_list.append(ade)

            # Find the minimum ADE
            min_ade = np.min(ade_list)
            min_ade_list.append(min_ade)

            if result[i][j]['object_type'] == 'TYPE_VEHICLE':
                min_ade_vehicle.append(min_ade)
            elif result[i][j]['object_type'] == 'TYPE_PEDESTRIAN':
                min_ade_pedestrian.append(min_ade)
            elif result[i][j]['object_type'] == 'TYPE_CYCLIST':
                min_ade_cyclist.append(min_ade)
            elif result[i][j]['object_type'] == 'TYPE_DUMMY':
                min_ade_dummy.append(min_ade)

    # Calculate average minADE for each class and overall
    avg_min_ade = np.mean(min_ade_list) if min_ade_list else 0
    avg_min_ade_vehicle = np.mean(min_ade_vehicle) if min_ade_vehicle else 0
    avg_min_ade_pedestrian = np.mean(min_ade_pedestrian) if min_ade_pedestrian else 0
    avg_min_ade_cyclist = np.mean(min_ade_cyclist) if min_ade_cyclist else 0
    avg_min_ade_dummy = np.mean(min_ade_dummy) if min_ade_dummy else 0

    return {
        'overall_minADE': avg_min_ade,
        'vehicle_minADE': avg_min_ade_vehicle,
        'pedestrian_minADE': avg_min_ade_pedestrian,
        'cyclist_minADE': avg_min_ade_cyclist,
        'dummy_minADE': avg_min_ade_dummy
    }

def WeightedADE(result, num_modes=3):
    avg_weighted_ade = []
    avg_weighted_ade_vehicle = []
    avg_weighted_ade_pedestrian = []
    avg_weighted_ade_cyclist = []
    avg_weighted_ade_dummy = []
    for i in range(len(result)):
        for j in range(len(result[i])):
            pred_trajs = result[i][j]['pred_trajs']
            gt_trajs = result[i][j]['gt_trajs'][11:,:2]
            pred_scores = result[i][j]['pred_scores']
            
            top3_indices = np.argsort(pred_scores)[-num_modes:][::-1]
            top3_pred_trajs = pred_trajs[top3_indices]
            top3_scores = pred_scores[top3_indices]
            normalized_top3_scores = top3_scores / np.sum(top3_scores)

            # weighted ADE caldulation
            t_cut = 11
            T = 61
            weighted_ade = 0

            for k in range(top3_pred_trajs.shape[0]):
                distance = np.sum((gt_trajs - top3_pred_trajs[k])**2, axis=1)
                distance = np.sqrt(distance)
                weighted_ade += normalized_top3_scores[k] * distance

            weighted_ade = np.sum(weighted_ade)
            weighted_ade = weighted_ade / (T - t_cut)
            avg_weighted_ade += [weighted_ade]

            if result[i][j]['object_type'] == 'TYPE_VEHICLE':
                avg_weighted_ade_vehicle += [weighted_ade]
            elif result[i][j]['object_type'] == 'TYPE_PEDESTRIAN':
                avg_weighted_ade_pedestrian += [weighted_ade]
            elif result[i][j]['object_type'] == 'TYPE_CYCLIST':
                avg_weighted_ade_cyclist += [weighted_ade]
            elif result[i][j]['object_type'] == 'TYPE_DUMMY':
                avg_weighted_ade_dummy += [weighted_ade]
         

    avg_weighted_ade = np.mean(avg_weighted_ade)
    avg_weighted_ade_vehicle = np.mean(avg_weighted_ade_vehicle)
    avg_weighted_ade_pedestrian = np.mean(avg_weighted_ade_pedestrian)
    avg_weighted_ade_cyclist = np.mean(avg_weighted_ade_cyclist)
    avg_weighted_ade_dummy = np.mean(avg_weighted_ade_dummy)
    return avg_weighted_ade, avg_weighted_ade_vehicle, avg_weighted_ade_pedestrian, avg_weighted_ade_cyclist, avg_weighted_ade_dummy    

def check_vehicle_off_road(traj, map):
    road = map[map[..., 4] == 1]

    for i in range(traj.shape[0]):
        dist = np.linalg.norm(traj[i] - road[:, :2], axis=1)
        min_dist = np.min(dist)
        if min_dist > 4.0:
            return True

    return False

def check_vru_off_area(traj, map):
    sidewalk = map[map[..., 4] == 2]
    crosswalk = map[map[..., 4] == 3]
    area = np.concatenate([sidewalk, crosswalk], axis=0)

    for i in range(traj.shape[0]):
        dist = np.linalg.norm(traj[i] - area[:, :2], axis=1)
        min_dist = np.min(dist)
        if min_dist > 4.0:
            return True

    return False

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





## Begin testing pipeline
conflict_prediction = pd.DataFrame()
metric_ade_df = pd.DataFrame()


# allresultpred = []


# Iterate over all GT data
for file in tqdm(all_files):

    # if '_400' not in file:
    #     continue
    # breakpoint()
    object_id_start = 0
    data = pd.read_csv(file)

    info = {}
    info['file_id'] = file.split('/')[-1].split('_')[1]
    info['timestamps_seconds'] = list(data['Time'])
    info['prediction_scenarios'] = []  
    # total_track_infos, object_id_start = decode_tracks_from_csv(data, object_id_start, file)
    map_infos = decode_map_features_from_proto_mtr(vector_map.map_features)
    scenario_id = file.split('/')[-1].split('.')[0].replace('_GT', '')
    tqdm.write(f'Processing scenario {scenario_id}')

    timestamps_run = data['Time']
    conflict_pred = []
    figs = []
    
    # Iterate over all timestamps
    cut_off = len(timestamps_run) * 0.75
    for j, timestamp in enumerate(timestamps_run):
        # Skip start and end of scenario
        # if j < 10 or j >= len(timestamps_run) - 80:
        #     continue
        # if j < 200 or j >= len(timestamps_run) - 100:
        #     continue

        # # Skip interval
        # if j % interval != 0:
        #     continue
        if j != int(cut_off):
            continue

        filtered_data = data[data['Time'] <= timestamp]

        object_id_start = 0
        run_id = scenario_id.split('_')[1]

        total_track_infos, object_id_start = decode_tracks_from_csv(filtered_data, object_id_start, file, run_id=scenario_id)
        if len(total_track_infos['object_id']) == 0:
            print("no object with valid traj before timestamp")
            continue
        # get trajectory data, map data, and future GT data
        # raw_perception_data = data.iloc[:j+1]
        # trajectory_data, map_data = process_from_df(raw_perception_data, vector_map)
        start_timestamp = j - history_timesteps + 1
        future_timesteps = timestamps_run[j:j+50]
        prediction_info = create_info_single_prediction_scenario(info, total_track_infos, start_timestamp, map_infos,61, 10)

        if prediction_info == None:
            continue
        info['prediction_scenarios'].append(prediction_info)
          
        scene_id = prediction_info['scenario_id']
        sdc_track_index = prediction_info['tracks_to_predict']['track_index'][0]
        current_time_index = prediction_info['current_time_index']
        timestamps = np.array(prediction_info['timestamps_seconds'][:current_time_index + 1], dtype=np.float32)


        track_infos = prediction_info['track_infos']

        track_index_to_predict = np.array(prediction_info['tracks_to_predict']['track_index'])
        obj_types = np.array(track_infos['object_type'])
        obj_ids = np.array(track_infos['object_id'])
        obj_trajs_full = track_infos['trajs'].copy()  # (num_objects, num_timestamp, 10)
        future_zeros = np.zeros((obj_trajs_full.shape[0], 50, obj_trajs_full.shape[2]))
        obj_trajs_full = np.concatenate((obj_trajs_full, future_zeros), axis=1)
        obj_trajs_full[:, -50:, 9] = 1
        # obj_trajs_full[:, current_time_index + 1:, :] = np.zeros_like(obj_trajs_full[:, current_time_index + 1:, :])
        # obj_trajs_full[:,current_time_index+1:, 9] = 1

        obj_trajs_past = obj_trajs_full[:, :current_time_index + 1]
        obj_trajs_future = obj_trajs_full[:, current_time_index + 1:]

        center_objects, track_index_to_predict = get_interested_agents(
            track_index_to_predict=track_index_to_predict,
            obj_trajs_full=obj_trajs_full,
            current_time_index=current_time_index,
            obj_types=obj_types, scene_id=scene_id
        )

        (obj_trajs_data, obj_trajs_mask, obj_trajs_pos, obj_trajs_last_pos, obj_trajs_future_state, obj_trajs_future_mask, center_gt_trajs,
            center_gt_trajs_mask, center_gt_final_valid_idx,
            track_index_to_predict_new, sdc_track_index_new, obj_types, obj_ids) = create_agent_data_for_center_objects(
            center_objects=center_objects, obj_trajs_past=obj_trajs_past, obj_trajs_future=obj_trajs_future,
            track_index_to_predict=track_index_to_predict, sdc_track_index=sdc_track_index,
            timestamps=timestamps, obj_types=obj_types, obj_ids=obj_ids
        )

        ret_dict = {
            'scenario_id': np.array([scene_id] * len(track_index_to_predict)),
            'obj_trajs': obj_trajs_data,
            'obj_trajs_mask': obj_trajs_mask,
            'track_index_to_predict': track_index_to_predict_new,  # used to select center-features
            'obj_trajs_pos': obj_trajs_pos,
            'obj_trajs_last_pos': obj_trajs_last_pos,
            'obj_types': obj_types,
            'obj_ids': obj_ids,

            'center_objects_world': center_objects,
            'center_objects_id': np.array(track_infos['object_id'])[track_index_to_predict],
            'center_objects_type': np.array(track_infos['object_type'])[track_index_to_predict],

            'obj_trajs_future_state': obj_trajs_future_state,
            'obj_trajs_future_mask': obj_trajs_future_mask,
            'center_gt_trajs': center_gt_trajs,
            'center_gt_trajs_mask': center_gt_trajs_mask,
            'center_gt_final_valid_idx': center_gt_final_valid_idx,
            'center_gt_trajs_src': obj_trajs_full[track_index_to_predict]
        }

        map_polylines_data, map_polylines_mask, map_polylines_center = create_map_data_for_center_objects(
                center_objects=center_objects, map_infos=prediction_info['map_infos'],
                center_offset=dataset_cfg.get('CENTER_OFFSET_OF_MAP', (30.0, 0)), dataset_cfg = dataset_cfg
            )   # (num_center_objects, num_topk_polylines, num_points_each_polyline, 9), (num_center_objects, num_topk_polylines, num_points_each_polyline)

        ret_dict['map_polylines'] = map_polylines_data
        ret_dict['map_polylines_mask'] = (map_polylines_mask > 0)
        ret_dict['map_polylines_center'] = map_polylines_center
        for key, val in ret_dict.items():
                if key in ['obj_trajs', 'obj_trajs_mask', 'map_polylines', 'map_polylines_mask', 'map_polylines_center',
                                'obj_trajs_pos', 'obj_trajs_last_pos', 'obj_trajs_future_state', 'obj_trajs_future_mask', 
                                'center_gt_trajs','center_gt_trajs_mask','center_gt_final_valid_idx','center_objects_world', 'center_gt_trajs_src','track_index_to_predict']:
                                val = torch.from_numpy(val).to(device)
                                ret_dict[key] = val
        batch_dict = {'input_dict': ret_dict, 'batch_size': 1, 'batch_sample_count':[len(ret_dict['track_index_to_predict'])]}
        with torch.no_grad():
                batch_pred_dicts = model(batch_dict)
                final_pred_dicts = generate_prediction_dicts(batch_pred_dicts, output_path=None)
        
        # allresultpred.append(final_pred_dicts[0])
        
        # Iterate over all valid agents
        path_prediction_results = {}
        trajectory_data, map_data = process_from_df(filtered_data, vector_map, j+1)
        # future_gt_data = process_gt_from_df(data.iloc[j+1:j+51])


        for pred_i in final_pred_dicts[0]:
            cur_obj_id = pred_i['object_id']
            ki = cur_obj_id
            if ki >= len(trajectory_data.keys()):
                breakpoint()
            k = list(trajectory_data.keys())[ki]
            agent_trajectory_data = trajectory_data[k]

            if np.sum(agent_trajectory_data['valid'][-history_timesteps:]) < history_timesteps:
                continue
            # if np.sum(future_gt_data[k]['valid']) < 50:
            #     continue
            
            # assert np.array_equal(pred_i['gt_trajs'][-50:,:2], future_gt_data[k]['traj'])
            pred_trajs = pred_i['pred_trajs']
            pred_scores = pred_i['pred_scores']
            top3_indices = np.argsort(pred_scores)[-3:][::-1]
            top3_pred_trajs = pred_trajs[top3_indices]
            top3_scores = pred_scores[top3_indices]
            normalized_top3_scores = top3_scores / np.sum(top3_scores)



            # filter invalid predictions
   
            global_prediction_trajs, prediction_scores = filter_invalid_predictions(k, top3_pred_trajs, 
                                                                                    normalized_top3_scores, map_data_postprocess)

            path_prediction_results[k] = (global_prediction_trajs, prediction_scores)

        # plot results and save gif
        plt.figure(figsize=(10, 10))
        plot_vector_map()

        colors = ['r', 'g', 'b', 'c', 'm']
        for a_i, a in enumerate(path_prediction_results.keys()):
            plot_agent(trajectory_data[a]['traj'][-1], trajectory_data[a]['sub_class'], color=colors[a_i])
            plot_trajectory(path_prediction_results[a][0], color=colors[a_i])

        plt.title(f'Scenario {scenario_id}, Time {timestamp}')
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
                    result = {'Timestamps': c_t, 'ID': k, 'path_ID': 1, 'subclass': trajectory_data[k]['sub_class'].replace('_Dummy', ''),
                              'x_center': np.nan, 'y_center': np.nan, 'z_center': np.nan, 'x_length': np.nan,
                              'y_length': np.nan, 'z_length': np.nan, 'confidence_score': np.nan}
                    #prediction_df = pd.concat([prediction_df, pd.DataFrame(result, index=[0])], axis=0)
                
                else: # iterate over all paths
                    for p in range(path_prediction_results[k][0].shape[0]):
                        pred_pos = path_prediction_results[k][0][p][dt]
                        pred_score = path_prediction_results[k][1][p]
                        result = {'Timestamps': c_t, 'ID': k, 'path_ID': p+1, 'subclass': trajectory_data[k]['sub_class'].replace('_Dummy', ''),
                                  'x_center': pred_pos[0], 'y_center': pred_pos[1], 'z_center': trajectory_data[k]['zctr'],
                                  'x_length': trajectory_data[k]['x_len'], 'y_length': trajectory_data[k]['y_len'], 
                                  'z_length': trajectory_data[k]['z_len'], 'confidence_score': pred_score}
                        prediction_df = pd.concat([prediction_df, pd.DataFrame(result, index=[0])], axis=0)
        
        if not prediction_df.empty:
            prediction_df = prediction_df.sort_values(by=['ID', 'path_ID'])
            prediction_df.to_csv(f'{output_path}/{scenario_id}_{timestamp}.csv', index=False)
      
        # calculate conflict
        objects = {k: (trajectory_data[k]['sub_class'], (trajectory_data[k]['y_len'], trajectory_data[k]['x_len'])) 
                   for k in path_prediction_results.keys()}
        conflict, ttc, ru1_subclass, ru2_subclass = calculate_conflict(path_prediction_results, objects)
        conflict_timestamp = timestamp + ttc if conflict else None
        conflict_pred.append((conflict, conflict_timestamp, ru1_subclass, ru2_subclass))
        # exit()
    # print(scenario_id)
    # print("weighted ADE")
    # print(WeightedADE(allresultpred))
    # print("min ADE")
    # print(calculate_minADE(allresultpred))
    # print("weighted ADE, mode = 1")
    # print(WeightedADE(allresultpred, num_modes=1))
      # Save visualization as gif
    if save_vis:
        imageio.mimsave(f'./{scenario_id}.gif', figs, duration=0.1*interval)
    
    # Save conflict prediction results
    min_ttc = np.inf
    ru1_subclass = np.nan
    ru2_subclass = np.nan
    conflict = any([c[0] for c in conflict_pred])

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



conflict_prediction.to_csv(output_path + '/' + 'conflict_prediction_results.csv', index=False)


# print("weighted ADE")
# print(WeightedADE(allresultpred))
# print("min ADE")
# print(calculate_minADE(allresultpred))
# print("weighted ADE, mode = 1")
# print(WeightedADE(allresultpred, num_modes=1))