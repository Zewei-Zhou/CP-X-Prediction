import numpy as np
import os
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from Prediction.conflict_prediction.conflict_prediction import generate_movement_polygon, get_conflict_point

def_collision_points = {'4': [6.5, -10.0],
                        '1': [20.0, -25.0],
                        '3': [26, -16.1],
                        '2': [14.0, -2.0]}
dis_threshold = 1
expansion_distance = 3.5
def_interaction_type = {'n2w', 'n2e', 'n2s', 's2w', 's2e', 's2n'}


def ttc_analysis(info_all):
    # set the analysis record
    ttc_statistic = {'VRU_Child_Dummy': {'ttc': [], 'disp': [],
                                         'collision_pos': [],
                                         'scenario_id': [],
                                         'interaction_type': []},
                     'VRU_Adult_Dummy': {'ttc': [], 'disp': [],
                                         'collision_pos': [],
                                         'scenario_id': [],
                                         'interaction_type': []},
                     'VRU_Adult_Using_Motorized_Bicycle_Dummy': {'ttc': [], 'disp': [],
                                                                 'collision_pos': [],
                                                                 'scenario_id': [],
                                                                 'interaction_type': []}}

    for scenario_id, info in info_all.items():
        object_type_class = info['object_type_class']
        object_type_subclass = info['object_type_subclass']

        trajs_data = np.array(info['trajs'], dtype=float)
        traj = trajs_data[:, :, :2]
        width = trajs_data[:, :, 3:4]
        length = trajs_data[:, :, 4:5]
        yaw = trajs_data[:, :, 6:7]
        vel = trajs_data[:, :, 7:9]

        # determine the interaction dummy index
        try:
            dummy_index = object_type_class.index('Dummy')
        except ValueError:
            print(f"no 'Dummy' or 'Vehicle' in the run {scenario_id}")
            continue

        vehicle_index = [index for index, type_class in
                         enumerate(object_type_class) if type_class == 'Vehicle']

        # generate polygon
        polygon_list = []
        for i in vehicle_index + [dummy_index]:
            valid_t = trajs_data[i, :, -1] > 0
            movement_polygon = generate_movement_polygon(traj[i, valid_t, :], width[i, valid_t, :],
                                                         length[i, valid_t, :],
                                                         yaw[i, valid_t, :])
            polygon_list.append(movement_polygon)

        # identify path overlap
        overlap_pair_id = []
        overlap_area = []
        for i in range(len(vehicle_index)):
            overlap = polygon_list[i].intersects(polygon_list[-1])
            if overlap:
                overlap_area.append(polygon_list[i].intersection(polygon_list[-1]))
                overlap_pair_id.append([vehicle_index[i], dummy_index])

        # determine the timestamp of dummy start
        v_dummy = np.sqrt(np.square(vel[dummy_index, :, 0]) + np.square(vel[dummy_index, :, 1]))
        start_t = detect_start_timestamp(v_dummy)

        # analyze overlap condition and calculate ttc
        for i in range(len(overlap_pair_id)):

            object_a = overlap_pair_id[i][0]
            object_b = overlap_pair_id[i][1]

            conflict_point_a, conflict_t_a = get_conflict_point(traj[object_a, :, :], overlap_area[i])
            conflict_point_b, conflict_t_b = get_conflict_point(traj[object_b, :, :], overlap_area[i])

            # assumption: dummy exists in the scenario all the time
            veh_valid_t = np.where(trajs_data[object_a, :, -1] > 0)[0]
            if conflict_t_a > conflict_t_b:
                # dummy go first
                if veh_valid_t[0] > start_t:
                    continue
            elif veh_valid_t[-1] < start_t:
                # vehicle first
                continue

            ttc, disp = calculate_ttc(traj[object_a, start_t, :], traj[object_b, start_t, :], conflict_point_a, \
                                      vel[object_a, start_t, :], vel[object_b, start_t, :])

            # filter the high ttc
            if ttc > 10:
                ttc = 10

            # harding coding, filter 805, which have two ttc because wrong heading
            if ttc < -6.5:
                continue

            # determine the interaction type (based on the start point, hard coding)
            valid_t = np.argmax(trajs_data[vehicle_index[i], :, -1] > 0)
            if conflict_point_a.x < 12:
                if traj[vehicle_index[i], valid_t, 1] > 10:
                    interaction_type = 'n2w'
                else:
                    interaction_type = 's2w'
            elif conflict_point_a.x > 22:
                if traj[vehicle_index[i], valid_t, 1] > 10:
                    interaction_type = 'n2e'
                else:
                    interaction_type = 's2e'
            else:
                if traj[vehicle_index[i], valid_t, 1] > 10:
                    interaction_type = 'n2s'
                else:
                    interaction_type = 's2n'

            dummy_subclass = object_type_subclass[dummy_index]
            ttc_statistic[dummy_subclass]['ttc'].append(ttc)
            ttc_statistic[dummy_subclass]['disp'].append(disp)
            ttc_statistic[dummy_subclass]['collision_pos'].append(conflict_point_a)
            ttc_statistic[dummy_subclass]['scenario_id'].append(scenario_id)
            ttc_statistic[dummy_subclass]['interaction_type'].append(interaction_type)

    # plot_analysis_results(ttc_statistic)

    # hard coding for error filtering
    ttc_statistic['VRU_Child_Dummy'] = \
        remove_unusual_ttc(ttc_statistic['VRU_Child_Dummy'], 6, 1)
    ttc_statistic['VRU_Adult_Using_Motorized_Bicycle_Dummy'] = \
        remove_unusual_ttc(ttc_statistic['VRU_Adult_Using_Motorized_Bicycle_Dummy'], 5)
    ttc_statistic['VRU_Adult_Using_Motorized_Bicycle_Dummy'] = \
        remove_unusual_ttc(ttc_statistic['VRU_Adult_Using_Motorized_Bicycle_Dummy'], 0.1, -0.1, False)

    ttc_modes = cluster_ttc(ttc_statistic)
    return ttc_modes


def detect_start_timestamp(velocity):
    time_gap = 30  # hardcode
    v_threshold = 0.5
    time_disp = 0.1  # 10 Hz, hardcode
    acc = (velocity[1:] - velocity[:-1]) / time_disp
    acc = np.concatenate(([acc[0]], acc[:]))

    index = np.where(acc > 0)[0]
    if len(index) == 0:
        time_step = len(velocity) - 1
    else:
        for time_step in index:
            time_end = min(time_step + time_gap, len(velocity) - 1)
            if velocity[time_end] > v_threshold:
                break
    return time_step


def calculate_ttc(traj1, traj2, conflict_point, v1, v2):
    rel_pos1 = [conflict_point.x, conflict_point.y] - traj1[:]
    rel_vel1 = v1
    rel_pos2 = [conflict_point.x, conflict_point.y] - traj2[:]
    rel_vel2 = v2
    norm_rel_vel_sq1 = np.linalg.norm(rel_vel1) ** 2

    ttc = np.dot(rel_pos1, rel_vel1) / (norm_rel_vel_sq1 + 1e-5)

    return ttc, np.linalg.norm(rel_pos1)


def remove_unusual_ttc(dummy_data, ttc_threshold_max=None, ttc_threshold_min=None, keep_centerband=True):

    if ttc_threshold_max is not None:
        indices = [i for i, ttc in enumerate(dummy_data['ttc'])
                             if ttc > ttc_threshold_max]

    if ttc_threshold_min is not None:
        indices += [i for i, ttc in enumerate(dummy_data['ttc'])
                              if ttc < ttc_threshold_min]

    for key in dummy_data:
        if keep_centerband:
            dummy_data[key] = [value for i, value in enumerate(dummy_data[key])
                               if i not in indices]
        else:
            dummy_data[key] = [value for i, value in enumerate(dummy_data[key])
                               if i in indices]

    return dummy_data

def cluster_ttc(data):
    cluster_centers = {}
    for obj_class, stats in data.items():
        n_clusters = 2 if obj_class == 'VRU_Child_Dummy' else 3
        ttc_array = np.array(stats['ttc']).reshape(-1, 1)
        kmeans = KMeans(n_clusters=n_clusters, random_state=0).fit(ttc_array)

        centers = kmeans.cluster_centers_.flatten()
        cluster_centers[obj_class] = {f'mode_{i}': centers[i] for i in range(n_clusters)}

    return cluster_centers


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

            try:
                id_index = ttc_statistic[dummy_subclass]['scenario_id'].index(scene)
            except ValueError:
                continue
            collision_pos = ttc_statistic[dummy_subclass]['collision_pos'][id_index]
            ax.plot(collision_pos.x, collision_pos.y, marker='x', markersize=10)

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


def plot_analysis_results(ttc_statistic):
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10), sharex='col', sharey='row')
    categories = list(ttc_statistic.keys())

    for i, category in enumerate(categories):
        ax = axes[0, i]
        scenario_ids = ttc_statistic[category]['scenario_id']
        bars = ax.bar(np.arange(len(ttc_statistic[category]['ttc'])), ttc_statistic[category]['ttc'])
        ax.set_title(f'TTC Profiles for {category}')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('TTC')

        for bar, scenario_id in zip(bars, scenario_ids):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    scenario_id, ha='center', va='bottom')

    for i, category in enumerate(categories):
        ax = axes[1, i]
        scenario_ids = ttc_statistic[category]['scenario_id']
        ax.bar(np.arange(len(ttc_statistic[category]['disp'])), ttc_statistic[category]['disp'], color='orange')
        ax.set_title(f'Disp Profiles for {category}')
        ax.set_xlabel('Disp Steps')
        ax.set_ylabel('Disp')

        for bar, scenario_id in zip(bars, scenario_ids):
            ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
                    scenario_id, ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

    # Plot TTC by interaction type
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12), sharex='col', sharey='row')
    bar_width = 0.2
    for i, interaction_type in enumerate(def_interaction_type):
        ax = axes[i // 3, i % 3]
        for j, category in enumerate(categories):
            ttc_values = [ttc_statistic[category]['ttc'][k] for k in range(len(ttc_statistic[category]['ttc']))
                          if ttc_statistic[category]['interaction_type'][k] == interaction_type]
            positions = np.arange(len(ttc_values)) + j * bar_width
            ax.bar(positions, ttc_values, bar_width, label=category)
        ax.set_title(f'TTC Profiles for {interaction_type}')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('TTC')
        ax.legend()

    plt.tight_layout()
    plt.show()

    # Plot disp by interaction type
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 12), sharex='col', sharey='row')
    bar_width = 0.2
    for i, interaction_type in enumerate(def_interaction_type):
        ax = axes[i // 3, i % 3]
        for j, category in enumerate(categories):
            ttc_values = [ttc_statistic[category]['disp'][k] for k in range(len(ttc_statistic[category]['disp']))
                          if ttc_statistic[category]['interaction_type'][k] == interaction_type]
            positions = np.arange(len(ttc_values)) + j * bar_width
            ax.bar(positions, ttc_values, bar_width, label=category)
        ax.set_title(f'Disp Profiles for {interaction_type}')
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Disp')
        ax.legend()

    plt.tight_layout()
    plt.show()

    return 0
