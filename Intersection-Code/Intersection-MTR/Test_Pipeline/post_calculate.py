import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from test_utils import *
from data_utils import *


# Load the data
results_path = "mtr_result_rehearsal_3"
results_files = glob.glob(results_path + "/*.csv")
trajectory_path = "../Data/rehearsal_3"
trajectory_files = glob.glob(trajectory_path + "/*.csv")
# trajectory_files = ['../Data/validation_GT_second_release/Run_179_GT.csv','../Data/validation_GT_second_release/Run_315_GT.csv','../Data/validation_GT_second_release/Run_214_GT.csv','../Data/validation_GT_second_release/Run_410_GT.csv','../Data/validation_GT_second_release/Run_1078_GT.csv','../Data/validation_GT_second_release/Run_91_GT.csv','../Data/validation_GT_second_release/Run_448_GT.csv',\
#              '../Data/validation_GT_second_release/Run_875_GT.csv', '../Data/validation_GT_second_release/Run_48_GT.csv','../Data/validation_GT_second_release/Run_363_GT.csv']
conflict_file = 'results_output_mtr_rehearsal/conflict_prediction_results.csv'
# modified_results_path = "./results_output_modified"
# modified_results_files = glob.glob(modified_results_path + "/*.csv")

# Go through all the prediction files
metric_ade_df = pd.DataFrame()

for file in results_files:
    if 'conflict' in file:
        continue
    if 'ADE' in file:
        continue
    r = pd.read_csv(file)
    scenario_id = file.split('/')[-1].split('_')[0] + '_' + file.split('/')[-1].split('_')[1]
    print(f"Loading scenario {scenario_id}")

    predict_time_steps = r['Timestamps'].unique()

    # load gt data
    # if len([f for f in trajectory_files if scenario_id + '_' in f]) != 1:
    #     breakpoint()

    gt_file = [f for f in trajectory_files if scenario_id + '_' in f][0]
    gt_data = pd.read_csv(gt_file)
    
    # select gt time steps
    gt_data = gt_data[gt_data['Time'].isin(predict_time_steps)]
    if len(gt_data) == 0:
        print(f"No ground truth data for scenario {scenario_id}")
        continue
    csv_keygroup = get_object_keygroups(gt_data)

    gt_trajectory_data = {}
    for key, group in csv_keygroup.items():
        id = key.replace('_xctr', '')
        x = gt_data[group[0]].values
        y = gt_data[group[1]].values
        traj = np.stack([x, y], axis=1)
        traj = np.nan_to_num(traj)
        gt_trajectory_data[id] = traj

    pred_trajectory_data = {}
    for a in r['ID'].unique():
        agent_data = r[r['ID'] == a]
        trajectory_data = [agent_data[id==agent_data['path_ID']] for id in agent_data['path_ID'].unique()]
        trajectory_data_array = [np.array([t['x_center'], t['y_center']]).T for t in trajectory_data]
        trajectory_confidence = [np.array(t['confidence_score'])[0] for t in trajectory_data]
        pred_trajectory_data[a] = (trajectory_data_array, trajectory_confidence)

    for k in pred_trajectory_data.keys():
        fut_trajs = gt_trajectory_data[k]
        fut_valid = np.not_equal(fut_trajs[..., 0], 0)
        prediction_trajs, prediction_scores = pred_trajectory_data[k]
        prediction_trajs = np.stack(prediction_trajs, axis=0)
        prediction_scores = np.array(prediction_scores)

        error = np.linalg.norm(prediction_trajs[..., :2] - fut_trajs[None, :, :], axis=-1)
        error = error * fut_valid
        weighted_error = np.sum(error * prediction_scores[:, None], axis=0)
        ade = np.sum(weighted_error) / np.sum(fut_valid) if np.sum(fut_valid) > 0 else 0.0
        result = {'scenario_id': scenario_id, 'time': predict_time_steps[0], 'object': k, 'ADE': ade}
        metric_ade_df = pd.concat([metric_ade_df, pd.DataFrame(result, index=[0])], axis=0)
        print(f"Sceanrio {scenario_id}, Object {k}, ADE: {ade}")


# Weighted ADE
metric_ade_df.to_csv('weighted_ADE_results.csv', index=False)

ade_results = pd.read_csv('weighted_ADE_results.csv')
print(f'\nTrajectory Prediction == Total Weighted ADE: {ade_results["ADE"].mean()}')
dummy_ade_results = ade_results[ade_results['object'].str.contains('Dummy')]
print(f'Trajectory Prediction == Dummy Weighted ADE: {dummy_ade_results["ADE"].mean()}')
vehicle_ade_results = ade_results[ade_results['object'].str.contains('Vehicle')]
print(f'Trajectory Prediction == Vehicle Weighted ADE: {vehicle_ade_results["ADE"].mean()}')
vru_ade_results = ade_results[ade_results['object'].str.contains('VRU')]
vru_ade_results = vru_ade_results[['Dummy' not in x for x in vru_ade_results['object']]]
print(f'Trajectory Prediction == VRU Weighted ADE: {vru_ade_results["ADE"].mean()}')


### Conflict Prediction
print('\nConflict Prediction')
conflict_labels = pd.read_csv('conflict_no_conflict_labels_all_validation_runs.csv')
conflict_results = pd.read_csv(conflict_file)
FP, FN, TP, TN = 0, 0, 0, 0
runs = conflict_results['Run ID']

for run in runs:
    if run in conflict_labels['Run ID'].values:
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