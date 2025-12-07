import glob
import numpy as np
import pandas as pd
from conflict import calculate_conflict
import warnings
warnings.filterwarnings("ignore")

# Load the data
results_path = "./results_output"
results_files = glob.glob(results_path + "/*.csv")
trajectory_path = "./test_data"
trajectory_files = glob.glob(trajectory_path + "/*.csv")
conflict_labels = pd.read_csv('conflict_no_conflict_labels_all_validation_runs.csv')


# Go through all the prediction files
conflict_prediction = pd.DataFrame()

for file in results_files:
    result = pd.read_csv(file)
    scenario_id = file.split('/')[-1].split('_')[0] + '_' + file.split('/')[-1].split('_')[1]
    print(f"Loading scenario {scenario_id}")
    timestamp = result['Time'].unique()[0]
    print(f"Timestamp: {timestamp}")

    path_prediction_results = {}
    objects = {}
    for a in result['ID'].unique():
        agent_data = result[result['ID'] == a]
        trajectory_data = [agent_data[id==agent_data['path_ID']] for id in agent_data['path_ID'].unique()]
        trajectory_data_array = [np.array([t['x_center'], t['y_center']]).T for t in trajectory_data]
        trajectory_confidence = [np.array(t['confidence_score'])[0] for t in trajectory_data]
        path_prediction_results[a] = (trajectory_data_array, trajectory_confidence)
        objects[a] = (trajectory_data[0]['ID'].values[0], (0, 0))

    conflict, ttc, ru1_subclass, ru2_subclass = calculate_conflict(path_prediction_results, objects)
    conflict_timestamp = timestamp + ttc if conflict else None

    if ru1_subclass:
        if 'Dummy' in ru1_subclass:
            ru1_subclass = ru1_subclass.replace('_Dummy', '')
        if 'Vehicle' in ru1_subclass:
            ru1_subclass = ru1_subclass.replace('.1', '')
    if ru2_subclass:
        if 'Dummy' in ru2_subclass:
            ru2_subclass = ru2_subclass.replace('_Dummy', '')
        if 'Vehicle' in ru2_subclass:
            ru2_subclass = ru2_subclass.replace('.1', '')

    print(f"Conflict: {conflict}, Timestamp: {conflict_timestamp}, RU1 Subclass: {ru1_subclass}, RU2 Subclass: {ru2_subclass}")

    result = {'Run ID': scenario_id, 'Time': timestamp, 'Conflict_No_Conflict_Label': 'conflict' if conflict else 'no conflict',
              'timestamp_conflict': conflict_timestamp, 'road_user1_subclass': ru1_subclass, 'road_user2_subclass': ru2_subclass}
    conflict_prediction = pd.concat([conflict_prediction, pd.DataFrame(result, index=[0])], axis=0)
    

# Save the conflict prediction
conflict_prediction.to_csv("conflict_prediction.csv", index=False)

# Report the conflict prediction
conflict_labels = pd.read_csv('conflict_no_conflict_labels_all_validation_runs.csv')
FP, FN, TP, TN = 0, 0, 0, 0
runs = conflict_prediction['Run ID'].unique()

for run in runs:
    if run in conflict_labels['Run ID'].values:
        pred = conflict_prediction[conflict_prediction['Run ID'] == run]['Conflict_No_Conflict_Label']
        if any(pred == 'conflict'):
            pred = 'conflict'
        else:
            pred = 'no conflict'

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

