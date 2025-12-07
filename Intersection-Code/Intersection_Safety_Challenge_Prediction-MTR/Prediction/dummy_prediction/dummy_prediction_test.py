import pandas as pd
import numpy as np
import warnings
import os
import matplotlib.pyplot as plt
import uuid
from data_preprocess import create_infos_from_csv
from speed_profile_analysis import speed_profile_analysis
from dummy_ttc_analysis_2 import *
import pickle
from dummy_prediction import *
from dummy_track_analysis import *
import pandas as pd
from IPython.display import display
import glob

dummy_motion_phase = {'initial_static': 0,
                      'acceleration': 1,
                      'cruise': 2,
                      'deceleration': 3,
                      'end_static': 4}

# Data
prefix = "/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/rehearsal_3/group_a"
all_files = glob.glob(f'{prefix}/*.csv')

# Parameters
output_path = '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/rehearsal_3/group_a/dummy_output'
os.makedirs(output_path, exist_ok=True)
interval = 20
save_vis = False
save_csv = False

# load processed scenarios
with open('./processed_scenarios/info_all.pkl', 'rb') as file:
    info_all = pickle.load(file)
with open('./processed_scenarios/info_reh_a.pkl', 'rb') as file:
    info_reh = pickle.load(file)

# analyze the dummy path and spped profile
track_end_points, track_start_points = dummy_track_analysis(info_all)
# speed_mode_para = speed_profile_analysis(info_all)
with open('./processed_scenarios/speed_mode_para.pkl', 'rb') as file:
    speed_mode_para = pickle.load(file)

# ttc distribution
ttc_modes = ttc_analysis(info_all)

# draw the check results
# draw_scenario_with_collision_point(info_all, ttc_statistic)

# loop the test runs
# test_runs = ['469', '971', '214', '410', '91', '448', '48', '363', '773', '1228', '1229', '179', '315', '1078', '875']
# test_runs = ['214', '410', '91', '448', '48', '363', '179', '315', '1078', '875']
weighted_ade_list = []
for run_id, info in info_reh.items():
    if 'Dummy' not in info['object_type_class']: # or run_id not in test_runs
        continue
    prediction_scenarios = info['prediction_scenarios']
    count = 0

    # loop all the scenarios
    for j, prediction_scenario in enumerate(prediction_scenarios):
        # Skip start and end of scenario
        # if j < 100 or j >= len(prediction_scenarios) - 100:
        #     continue

        # dummy should keep in the scenario all the time
        dummy_index = prediction_scenario['object_type_class'].index('Dummy')
        dummy_subclass = prediction_scenario['object_type_subclass'][dummy_index]
        current_time_index = prediction_scenario['current_time_index']
        trajectory_data = prediction_scenario['trajs']

        if np.isnan(trajectory_data[dummy_index, :, 0]).any():
            continue

        path_end_point, track_position, phase = \
            dummy_path_prediction(prediction_scenario,
                                  track_end_points,
                                  track_start_points,
                                  dummy_motion_phase)

        pred_dummy_trajs, pred_gt_traj = dummy_speed_prediction(prediction_scenario,
                                                                path_end_point,
                                                                track_position,
                                                                phase,
                                                                ttc_modes,
                                                                speed_mode_para)

        # calculate the metrics
        # ade_per_mode = []
        # for mode_traj in pred_dummy_trajs:
        #     ade = np.mean(np.linalg.norm(mode_traj - pred_gt_traj, axis=1))
        #     ade_per_mode.append(ade)
        #
        # weighted_ade = np.nanmean(ade_per_mode)
        # weighted_ade_list.append(weighted_ade)

        # save path prediction results in csv
        if save_csv:
            prediction_df = pd.DataFrame()

            timestamps = prediction_scenario['timestamps_seconds']
            future_timesteps = timestamps[current_time_index + 1:]

            for dt, c_t in enumerate(future_timesteps):
                if len(pred_dummy_trajs) == 0:
                    result = {'Timestamps': c_t, 'ID': dummy_subclass, 'path_ID': 1, 'subclass': dummy_subclass,
                              'x_center': np.nan, 'y_center': np.nan, 'z_center': np.nan, 'x_length': np.nan,
                              'y_length': np.nan, 'z_length': np.nan, 'confidence_score': np.nan}
                    # prediction_df = pd.concat([prediction_df, pd.DataFrame(result, index=[0])], axis=0)

                else:  # iterate over all paths
                    for p in range(len(pred_dummy_trajs)):
                        pred_pos = pred_dummy_trajs[p][dt]
                        pred_score = 1 / len(pred_dummy_trajs)
                        result = {'Timestamps': c_t, 'ID': dummy_subclass, 'path_ID': p + 1,
                                  'subclass': dummy_subclass,
                                  'x_center': pred_pos[0], 'y_center': pred_pos[1],
                                  'z_center': trajectory_data[dummy_index, 0, :][2],
                                  'x_length': trajectory_data[dummy_index, 0, :][3], 'y_length': trajectory_data[dummy_index, 0, :][4],
                                  'z_length': trajectory_data[dummy_index, 0, :][5], 'confidence_score': pred_score}
                        prediction_df = pd.concat([prediction_df, pd.DataFrame(result, index=[0])], axis=0)

            # save results
            # use path_id to reorganize the dataframe
            if not prediction_df.empty:
                prediction_df = prediction_df.sort_values(by=['ID', 'path_ID'])
                if count % 20 == 0:
                    prediction_df.to_csv(f'{output_path}/{run_id}_{timestamps[current_time_index]}.csv', index=False)

            count += 1

# average ade and display
weighted_ade = np.nanmean(weighted_ade_list)
num_nan = np.isnan(weighted_ade_list).sum()
total_samples = len(weighted_ade_list)
data = {
    'Metric': ['Weighted ADE', 'Non-NaN Count', 'Total Samples'],
    'Value': [weighted_ade, num_nan, total_samples]
}
df = pd.DataFrame(data)
display(df)
