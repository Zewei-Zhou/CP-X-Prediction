import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from test_utils import *
from data_utils import *

model_1_results_path = "./MTR_Results"
model_2_results_path = "./QCNet_Results"
model_3_results_path = None
modified_results_path = "./Fused_Results"
os.makedirs(modified_results_path, exist_ok=True)

# Load the perception data
test_data_path = "./test_data"
test_data_files = glob.glob(test_data_path + "/*.csv")

# Functions
def write_to_csv(data, timesteps, filename):
    """
    Write the data to a csv file.
    
    Args:
        data: the data to write (Dictionary of trajectories)
        timesteps: time steps
        filename: the filename to write to csv
    """
    with open(os.path.join(modified_results_path, filename), 'w') as f:
        f.write("Timestamps,ID,subclass,path_ID,x_center,y_center,z_center,x_length,y_length,z_length,confidence_score\n")
        for i, time in enumerate(timesteps):
            for j, agent in enumerate(data):
                for k, trajectory in enumerate(data[agent][0]):
                    t = time
                    id = data[agent][2]
                    sub_class = data[agent][3]
                    path_ID = k + 1
                    x_center = trajectory[i][0]
                    y_center = trajectory[i][1]
                    z_center = trajectory[i][2]
                    x_length = trajectory[i][3]
                    y_length = trajectory[i][4]
                    z_length = trajectory[i][5]
                    confidence_score = data[agent][1][k] / np.sum(data[agent][1])
                    f.write(f"{t},{id},{sub_class},{path_ID},{x_center},{y_center},{z_center},{x_length},{y_length},{z_length},{confidence_score}\n")

    # reorder csv file based on the path_ID
    df = pd.read_csv(os.path.join(modified_results_path, filename))
    df = df.sort_values(by=['ID', 'path_ID'])
    df.to_csv(os.path.join(modified_results_path, filename), index=False)


## go through all the test data files
for file in test_data_files:
    scenario_id = file.split('/')[-1].split('_')[0] + '_' + file.split('/')[-1].split('_')[1]
    print(f"Loading scenario {scenario_id}")
    
    # load model 1 results
    print(glob.glob(model_1_results_path + "/*.csv"))
    model_1_results = pd.read_csv([f for f in glob.glob(model_1_results_path + "/*.csv") if scenario_id in f][0])
    predict_time_steps = model_1_results['Timestamps'].unique()
    agents = model_1_results['ID'].unique()

    # load model 2 results
    model_2_results = pd.read_csv([f for f in glob.glob(model_2_results_path + "/*.csv") if scenario_id in f][0])
    
    # select gt time steps
    current_data = pd.read_csv(file)
    current_data = current_data[current_data['Time'] < predict_time_steps[0]]
    
    csv_keygroup = get_object_keygroups(current_data)

    history_trajectory_data = {}
    for key, group in csv_keygroup.items():
        id = key.replace('_xctr', '')
        x = current_data[group[0]].values
        y = current_data[group[1]].values
        traj = np.stack([x, y], axis=1)
        traj = np.nan_to_num(traj)
        history_trajectory_data[id] = traj

    # visualize the trajectory data
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plot_vector_map()

    colors = ['r', 'g', 'b', 'c', 'm']
    model_1_trajectories = {}
    model_2_trajectories = {}

    for a_i, a in enumerate(agents):
        agent_data = model_1_results[model_1_results['ID'] == a]
        trajectory_data = [agent_data[id==agent_data['path_ID']] for id in agent_data['path_ID'].unique()]
        trajectory_data_array = [np.array([t['x_center'], t['y_center'],
                                           t['z_center'], t['x_length'],
                                           t['y_length'], t['z_length']]).T for t in trajectory_data]
        trajectory_confidence = [np.array(t['confidence_score'])[0] for t in trajectory_data]
        agent_start = history_trajectory_data[a][-1]
    
        plot_agent(agent_start, a, color=colors[a_i])
        plot_trajectory(history_trajectory_data[a], color=colors[a_i], history=True)
        plot_trajectory(trajectory_data_array, color=colors[a_i])
        model_1_trajectories[a] = (trajectory_data_array, trajectory_confidence, a, agent_data['subclass'].values[0])
        plt.text(trajectory_data_array[0][0][0], trajectory_data_array[0][0][1], str(a_i), fontsize=50, color='black', zorder=5)

    plt.title('Model 1')
    plt.xlim(-50, 70)
    plt.ylim(-80, 70)
    plt.gca().set_aspect('equal', adjustable='box')

    plt.subplot(1, 2, 2)
    plot_vector_map()

    for a_i, a in enumerate(agents):
        agent_data = model_2_results[model_2_results['ID'] == a]
        trajectory_data = [agent_data[id==agent_data['path_ID']] for id in agent_data['path_ID'].unique()]
        trajectory_data_array = [np.array([t['x_center'], t['y_center'],
                                           t['z_center'], t['x_length'],
                                           t['y_length'], t['z_length']]).T for t in trajectory_data]
        trajectory_confidence = [np.array(t['confidence_score'])[0] for t in trajectory_data]

        plot_agent(agent_start, a, color=colors[a_i])
        plot_trajectory(history_trajectory_data[a], color=colors[a_i], history=True)
        plot_trajectory(trajectory_data_array, color=colors[a_i])
        model_2_trajectories[a] = (trajectory_data_array, trajectory_confidence, a, agent_data['subclass'].values[0])
        plt.text(trajectory_data_array[0][0][0], trajectory_data_array[0][0][1], str(a_i), fontsize=50, color='black', zorder=5)

    plt.title('Model 2')
    plt.xlim(-50, 70)
    plt.ylim(-80, 70)
    plt.tight_layout()
    plt.gca().set_aspect('equal', adjustable='box')

    plt.show(block=False)

    # select results for each agent
    selected_trajectories = {}
    for i, k in enumerate(agents):
        prompt = f"Select the best prediction results for agent {i} -- {k} (Model 1 or 2): "
        best_model = int(input(prompt))
        while best_model not in [1, 2]:
            best_model = int(input("Invalid input. Please select 1 or 2: "))

        if best_model == 1:
            selected_trajectories[k] = model_1_trajectories[k]
        elif best_model == 2:
            selected_trajectories[k] = model_2_trajectories[k]
        else:
            raise ValueError("Invalid input. Please select 1 or 2")


    # write the selected trajectories to a csv file
    write_to_csv(selected_trajectories, predict_time_steps, f"{scenario_id}_Path_Prediction_Submission_File.csv")

