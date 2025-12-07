import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from test_utils import *


# Load the data
results_path = "/home/tianhui/Intersection_Safety_Challenge_Prediction/Pipeline_New/results_output_mtr_41"
results_files = glob.glob(results_path + "/*.csv")
modified_results_path = "/home/tianhui/Intersection_Safety_Challenge_Prediction/Pipeline_New/results_output_mtr_41_modified"
os.makedirs(modified_results_path, exist_ok=True)


# Functions
def write_to_csv(data, timesteps, filename):
    """
    Write the data to a csv file.
    
    Args:
        data: the data to write (Dictionary of trajectories)
        timesteps: time steps
        filename: the filename to write to
    """
    
    with open(os.path.join(modified_results_path, filename), 'w') as f:
        f.write("Time, sub_class, path_ID, x_center, y_center, confidence_score\n")
        for i, time in enumerate(timesteps):
            for j, agent in enumerate(data):
                for k, trajectory in enumerate(data[agent][0]):
                    t = time
                    sub_class = data[agent][2]
                    path_ID = k
                    x_center = trajectory[i][0]
                    y_center = trajectory[i][1]
                    confidence_score = data[agent][1][k] / np.sum(data[agent][1])
                    f.write(f"{t}, {sub_class}, {path_ID}, {x_center}, {y_center}, {confidence_score}\n")


def generate_trajectory(points, start):
    """
    Generate a trajectory based on the points and time steps.
    
    Args:
        points: the points to generate the trajectory
        time_steps: the time steps to generate the trajectory
    
    Returns:
        the generated trajectory
    """

    # Generate the trajectory
    time_steps = [0.1, 2.0, 4.0, 6.0, 8.0]
    trajectory_time = np.linspace(0.1, 8, 80)

    # interpolate the points
    x = [start[0]] + [p[0] for p in points]
    y = [start[1]] + [p[1] for p in points]
    f_x = interpolate.interp1d(time_steps, x, kind='cubic')
    f_y = interpolate.interp1d(time_steps, y, kind='cubic')
    new_x = f_x(trajectory_time)
    new_y = f_y(trajectory_time)
    trajectory = np.stack([new_x, new_y], axis=1)
    
    return trajectory


# Go through all the files and load the data
for file in results_files:
    r = pd.read_csv(file)
    scenario_id = file.split('/')[-1].split('_')[0] + '_' + file.split('/')[-1].split('_')[1]
    print(f"Loading scenario {scenario_id}")
    time_steps = r['Time'].unique()

    # visualize the trajectory data
    plt.close()
    plt.figure(figsize=(20, 20))
    plot_vector_map()

    colors = ['r', 'g', 'b', 'c', 'm']
    agents = r['sub_class'].unique()
    trajectories = {}
    agent_starts = {}

    for a_i, a in enumerate(agents):
        agent_data = r[r['sub_class'] == a]
        trajectory_data = [agent_data[id==agent_data['path_ID']] for id in agent_data['path_ID'].unique()]
        trajectory_data_array = [np.array([t['x_center'], t['y_center']]).T for t in trajectory_data]
        trajectory_confidence = [np.array(t['confidence_score'])[0] for t in trajectory_data]
        agent_start = trajectory_data_array[0][0]
        agent_starts[a_i] = agent_start
        plot_agent(agent_start, a, color=colors[a_i])
        plot_trajectory_new(trajectory_data_array, color=colors[a_i])
        trajectories[a_i] = (trajectory_data_array, trajectory_confidence, a)
        plt.text(trajectory_data_array[0][0][0], trajectory_data_array[0][0][1], str(a_i), fontsize=50, color='black', zorder=5)

    plt.title(f'Scenario {scenario_id}')
    plt.xlim(-40, 60)
    plt.ylim(-50, 50)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.show(block=False)

    # Prompt the user to determine if human correction is needed
    while True:
        prompt = input("Do you want to adjust the predictions? (y/n): ")
        add_trajectory = False

        print("You can input 'n' to cancel the wrong input")

        if prompt.lower() == 'y':
            prompt = input(f"Which agent do you want to adjust? 0 - {len(trajectories)-1}: ")
            if prompt.lower() == 'n':
                print("Cancel the wrong input")
                continue

            while not prompt.isdigit() or int(prompt) not in range(len(trajectories)):
                prompt = input(f"Please enter a valid number between 0 and {len(trajectories)-1}: ")
            
            agent = trajectories[int(prompt)]
            print(f"Adjusting agent {agent[2]}")

            # Prompt the user to add or remove a trajectory
            prompt = input(f"Which trajectory do you want to remove? 0 - {len(agent[0])-1}: ")
            if prompt.lower() == 'n':
                print("Cancel the wrong input")
                continue

            while not prompt.isdigit() or int(prompt) not in range(len(agent[0])):
                prompt = input(f"Please enter a valid number between 0 and {len(agent[0])-1}: ")
      
            # Remove the trajectory
            agent[0].pop(int(prompt))
            agent[1].pop(int(prompt))

            # plot the new scenario
            plt.close()
            plt.figure(figsize=(20, 20))
            plot_vector_map()
            colors = ['r', 'g', 'b', 'c', 'm']

            for a_i, a in enumerate(trajectories):
                plot_agent(agent_starts[a_i], trajectories[a_i][2], color=colors[a_i])
                if trajectories[a_i][0] == []:
                    add_trajectory = True
                    agent_id = a_i
                    continue  
                   
                plot_trajectory_new(trajectories[a_i][0], color=colors[a_i])
                plt.text(trajectories[a_i][0][0][0][0], trajectories[a_i][0][0][0][1], str(a_i), fontsize=50, color='black', zorder=5)

            plt.title(f'Scenario {scenario_id}')
            plt.xlim(-40, 60)
            plt.ylim(-50, 50)
            plt.gca().set_aspect('equal', adjustable='box')
            plt.tight_layout()
            plt.show(block=False)

            if add_trajectory:
                print(f"Pleses add a new trajectory by selecting four points on the map for {trajectories[agent_id][2]}")
                prompt = input("Please adjust the view and press enter to continue")
                new_trajectory = []

                for i in range(4):
                    for a_i, a in enumerate(trajectories):
                        plot_agent(agent_starts[a_i], trajectories[a_i][2], color=colors[a_i])
                        if a_i == agent_id:
                            continue
                        
                        plot_trajectory_new(trajectories[a_i][0], color=colors[a_i])
                        plt.text(trajectories[a_i][0][0][0][0], trajectories[a_i][0][0][0][1], str(a_i), fontsize=50, color='black', zorder=5)

                    x, y = plt.ginput(1)[0]
                    new_trajectory.append([x, y])
                    plt.scatter(x, y, color=colors[agent_id], s=100, zorder=4)
                    plt.text(x, y, f"{(i+1)*2} s", fontsize=20, color='black', zorder=5)
                
                new_trajectory = generate_trajectory(new_trajectory, agent_starts[agent_id])
                trajectories[agent_id][0].append(new_trajectory)
                trajectories[agent_id][1].append(1.0)
                plot_trajectory_new([new_trajectory], color=colors[agent_id]) # plot the new trajectory
                plt.text(40, -40, 'New trajectory added!', fontsize=40, color='black', zorder=5)
                plt.show(block=False)

        # keep the original predictions
        elif prompt.lower() == 'n': 
            print("Keeping the original predictions")
            write_to_csv(trajectories, time_steps, file.split('/')[-1])
            break

        else:
            print("Please enter a valid response (y/n)")
            continue
    break

   