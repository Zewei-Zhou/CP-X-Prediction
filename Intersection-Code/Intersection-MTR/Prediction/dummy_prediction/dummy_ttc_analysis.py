import pandas as pd
import numpy as np
import warnings
import os
import matplotlib.pyplot as plt
import uuid

def_collision_points = {'west': [6.5, -10.0],
                        'south': [20.0, -25.0],
                        'east': [26.5, -16.1]}
dis_threshold = 1
expansion_distance = 3.5


def ttc_analysis(info_all):
    # set the analysis record
    ttc_statistic = {'VRU_Child_Dummy': {'ttc': [], 'disp': [], 'collision_pos': [], 'scenario_id': []},
                     'VRU_Adult_Dummy': {'ttc': [], 'disp': [], 'collision_pos': [], 'scenario_id': []},
                     'VRU_Adult_Using_Motorized_Bicycle_Dummy': {'ttc': [], 'disp': [], 'collision_pos': [], 'scenario_id': []}}

    for scenario_id, info in info_all.items():
        object_type_class = info['object_type_class']
        object_type_subclass = info['object_type_subclass']
        trajs = np.array(info['trajs'], dtype=float)

        try:
            dummy_index = object_type_class.index('Dummy')
        except ValueError:
            print(f"no 'Dummy' or 'Vehicle' in the run {scenario_id}")
            continue

        dummy_traj = trajs[dummy_index, :, :]
        dummy_subclass = object_type_subclass[dummy_index]
        vehicle_trajs = [trajs[index, :, :] for index, type_class
                         in enumerate(object_type_class) if type_class == 'Vehicle']

        # determine the collision point for each scenario
        # assumption: dummy exists in the scenario all the time
        min_distance = np.inf
        for collision_point_pos, collision_point in def_collision_points.items():
            total_distance = np.sum(
                np.sum(np.square(dummy_traj[:, :2] - collision_point), axis=1))
            if total_distance < min_distance:
                min_distance = total_distance
                cur_collision_point = collision_point
                cur_collision_point_pos = collision_point_pos

        # determine the target vehicle and find the closest point
        for vehicle_traj in vehicle_trajs:
            distance = np.sqrt(np.sum(np.square(
                vehicle_traj[:, :2] - cur_collision_point), axis=1))
            min_distance = np.nanmin(distance)
            veh_collision_timestamp = np.where(distance == min_distance)[0][0]
            if min_distance < dis_threshold:
                break

        # detect the start timestamp and collision timestamp
        v_dummy = np.sqrt(np.square(dummy_traj[:, 7]) + np.square(dummy_traj[:, 8]))
        start_timestamp = detect_start_timestamp(v_dummy)

        # calculate the ttc
        valid_timestamp = np.where(vehicle_traj[:, -1] > 0)[0][0]
        disp_vehicle = np.sqrt(
            np.sum(np.square(vehicle_traj[1:, :2] - vehicle_traj[:-1, :2]), axis=1))
        disp_vehicle[valid_timestamp:] = np.cumsum(disp_vehicle[valid_timestamp:])  # valid_timestamp in disp_vehicle is valid_timestamp+1 in vehicle_traj
        if valid_timestamp < start_timestamp:
            v_vehicle = np.sqrt(np.square(vehicle_traj[start_timestamp, 7])
                                + np.square(vehicle_traj[start_timestamp, 8]))
            disp = disp_vehicle[veh_collision_timestamp - 1] - disp_vehicle[start_timestamp - 1]
        else:
            # start_timestamp is out of the valid range
            v_vehicle = np.sqrt(np.square(vehicle_traj[valid_timestamp, 7])
                                + np.square(vehicle_traj[valid_timestamp, 8]))
            disp = (disp_vehicle[veh_collision_timestamp - 1] +
                    disp_vehicle[valid_timestamp] * (valid_timestamp - start_timestamp))

        ttc = disp / v_vehicle if v_vehicle != 0 else float('inf')
        ttc_statistic[dummy_subclass]['ttc'].append(ttc)
        ttc_statistic[dummy_subclass]['disp'].append(disp)
        ttc_statistic[dummy_subclass]['collision_pos'].append(cur_collision_point_pos)
        ttc_statistic[dummy_subclass]['scenario_id'].append(scenario_id)

    # draw the ttc
    # fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
    # for (category, ttc_list), ax in zip(ttc_statistic.items(), axes.flatten()):
    #     ax = axes[0, i]
    #     ax.bar(np.arange(len(ttc_list['ttc'])), ttc_list['ttc'], label=f'TTC for {category}')
    #     ax.set_title(f'TTC Profiles for {category}')
    #     ax.legend()
    #     ax.set_xlabel('Time Steps')
    #     ax.set_ylabel('TTC')
    #
    # for (category, ttc_list), ax in zip(ttc_statistic.items(), axes.flatten()):
    #     ax = axes[1, i]
    #     ax.bar(np.arange(len(ttc_list['disp'])), ttc_list['disp'], label=f'Disp for {category}')
    #     ax.set_title(f'Disp Profiles for {category}')
    #     ax.legend()
    #     ax.set_xlabel('Disp Steps')
    #     ax.set_ylabel('Disp')

    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10), sharex='col', sharey='row')
    categories = list(ttc_statistic.keys())

    for i, category in enumerate(categories):
        ax = axes[0, i]
        ax.bar(np.arange(len(ttc_statistic[category]['ttc'])), ttc_statistic[category]['ttc'])
        ax.set_title(f'TTC Profiles for {category}')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('TTC')

    for i, category in enumerate(categories):
        ax = axes[1, i]
        ax.bar(np.arange(len(ttc_statistic[category]['disp'])), ttc_statistic[category]['disp'], color='orange')
        ax.set_title(f'Disp Profiles for {category}')
        ax.set_xlabel('Disp Steps')
        ax.set_ylabel('Disp')

    plt.tight_layout()
    plt.show()

    return ttc_statistic


def detect_start_timestamp(velocity):
    time_gap = 30  # hardcode
    v_threshold = 0.5
    time_disp = 0.1  # 10 Hz, hardcode rn
    acc = (velocity[1:] - velocity[:-1]) / time_disp
    acc = np.concatenate(([acc[0]], acc))

    index = np.where(acc > 0)[0]
    for time_step in index:
        if velocity[time_step + time_gap] > v_threshold:
            break
    return time_step


def draw_scenario_with_collision_point(info_all, ttc_statistic):

    output_dir = '/Users/zewei/01_Projects/202405_Safety_challenge/output_collision_plots'
    os.makedirs(output_dir, exist_ok=True)

    for scene in info_all.keys():
        trajs = info_all[scene]['trajs']
        plt.figure()
        fig, ax = plt.subplots(figsize=(10, 15), dpi=300)

        for i in range(trajs.shape[0]):
            object_type_subclass = info_all[scene]['object_type_subclass'][i]
            valid_trajs = np.array([trajs[i, j, :2] for j in range(trajs.shape[1]) if trajs[i, j, -1] > 0])
            ax.plot(valid_trajs[:, 0], valid_trajs[:, 1],
                    linewidth=2.5, alpha=.9,
                    label=object_type_subclass if object_type_subclass not in ax.get_legend_handles_labels()[1] else "")
            ax.plot(valid_trajs[0, 0], valid_trajs[0, 1], marker='*', markersize=10)

        object_type_subclass = info_all[scene]['object_type_subclass']
        object_type_class = info_all[scene]['object_type_class']

        if 'Dummy' in object_type_class:
            dummy_index = object_type_class.index('Dummy')
            dummy_subclass = object_type_subclass[dummy_index]

            id_index = ttc_statistic[dummy_subclass]['scenario_id'].index(scene)
            collision_pos = ttc_statistic[dummy_subclass]['collision_pos'][id_index]
            ax.plot(def_collision_points[collision_pos], marker='x', markersize=10)

        ax.legend(fontsize='large')
        plt.tight_layout()
        ax.set_aspect('equal', adjustable='box')
        ax.set_title(f'Scene {scene}')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')

        output_file = os.path.join(output_dir, f'scene_{scene}.png')
        fig.savefig(output_file)
        plt.close(fig)

    return 0
