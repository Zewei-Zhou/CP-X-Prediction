import numpy as np
import matplotlib.pyplot as plt
import uuid
from scipy.optimize import curve_fit
from scipy.optimize import minimize
from scipy.optimize import differential_evolution
from scipy.optimize import dual_annealing
from sklearn.cluster import KMeans
import pickle
import os


def speed_profile_analysis(info_all):
    # assumption: dummy exists in each timestamp in each scenario
    # capture all dummy trajectories
    dummy_trajs = {'VRU_Child_Dummy': {},
                   'VRU_Adult_Dummy': {},
                   'VRU_Adult_Using_Motorized_Bicycle_Dummy': {}}
    for scenario_id, info in info_all.items():
        indices = [index for index, value in
                   enumerate(info['object_type_class']) if value == 'Dummy']
        trajs = info['trajs']
        for index in indices:
            dummy_trajs_type = \
                dummy_trajs[info['object_type_subclass'][index]]
            dummy_trajs_type.update({scenario_id: trajs[index, :, :]})

    # set the analysis record
    dummy_trajs_statistic = {'VRU_Child_Dummy':
                                 {'t_r': 0, 't_h': 0, 't_f': 0, 'a_r': 0, 'a_f': 0, 'V_max': 0},
                             'VRU_Adult_Dummy':
                                 {'t_r': 0, 't_h': 0, 't_f': 0, 'a_r': 0, 'a_f': 0, 'V_max': 0},
                             'VRU_Adult_Using_Motorized_Bicycle_Dummy':
                                 {'t_r': 0, 't_h': 0, 't_f': 0, 'a_r': 0, 'a_f': 0, 'V_max': 0}}

    # fit the trajectories
    fig, axes = plt.subplots(nrows=3, figsize=(10, 15))
    for (category, dummy_trajs_type), ax in zip(dummy_trajs.items(), axes.flatten()):
        statistic = dummy_trajs_statistic[category]
        t_r, t_h, t_f, a_r, a_f, V_max = [], [], [], [], [], []
        for scenario_id, traj in dummy_trajs_type.items():
            traj = np.array(traj, dtype=float)
            velocity = np.sqrt(np.square(traj[:, 7]) + np.square(traj[:, 8]))
            time_steps = np.arange(len(velocity))

            params = fit_velocity_profile(time_steps, velocity)
            fitted_velocity = trapezoid_model(time_steps, params)
            # ax.plot(time_steps, velocity, label=f'Scenario {scenario_id} Original', linewidth=2)
            # ax.plot(time_steps, fitted_velocity, label=f'Scenario {scenario_id} Fitted', linestyle='--')
            ax.plot(time_steps, velocity, linewidth=2)
            ax.plot(time_steps, fitted_velocity, linestyle='--')

            # record the params (a is based on timestamp not the absolute value)
            t_start_cur, t_r_cur, t_h_cur, t_f_cur, t_l_cur, V_max_cur = params
            t_r.append(t_r_cur)
            t_h.append(t_h_cur)
            t_f.append(t_f_cur)
            V_max.append(V_max_cur)
            a_r.append(V_max_cur / t_r_cur)
            a_f.append(V_max_cur / t_f_cur)

            # detect the start points
            # t_start_gt = detect_start_timestamp(velocity)

        statistic['t_r'] = t_r
        statistic['t_h'] = t_h
        statistic['t_f'] = t_f
        statistic['a_r'] = a_r
        statistic['a_f'] = a_f
        statistic['V_max'] = V_max
        # statistic['t_start_gt'] = t_start_gt

        ax.set_title(f'Velocity Profiles for {category}')
        ax.legend()
        ax.set_xlabel('Time Steps')
        ax.set_ylabel('Velocity')

    plt.tight_layout()
    plt.show()

    for category, statistic in dummy_trajs_statistic.items():
        # hard coding for error filtering
        if category == 'VRU_Child_Dummy':
            dummy_trajs_statistic['VRU_Child_Dummy'] = \
                remove_unusual_vmax(dummy_trajs_statistic['VRU_Child_Dummy'], 2)
        if category == 'VRU_Adult_Dummy':
            dummy_trajs_statistic['VRU_Adult_Dummy'] = \
                remove_unusual_vmax(dummy_trajs_statistic['VRU_Adult_Dummy'], 3)
        if category == 'VRU_Adult_Using_Motorized_Bicycle_Dummy':
            dummy_trajs_statistic['VRU_Adult_Using_Motorized_Bicycle_Dummy'] = \
                remove_unusual_vmax(dummy_trajs_statistic['VRU_Adult_Using_Motorized_Bicycle_Dummy'], 5)

        # t_r_avg = sum(statistic['t_r']) / len(statistic['t_r'])
        # t_h_avg = sum(statistic['t_h']) / len(statistic['t_h'])
        # t_f_avg = sum(statistic['t_f']) / len(statistic['t_f'])
        # a_r_avg = sum(statistic['a_r']) / len(statistic['a_r'])
        # a_f_avg = sum(statistic['a_f']) / len(statistic['a_f'])
        # V_max_avg = sum(statistic['V_max']) / len(statistic['V_max'])

        # hard coding for cluster 2 classes
        dummy_trajs_statistic[category] = cluster_dummy_data(statistic)

    # select the median of the a, and assume the a is the same in the acceleration and deceleration
    speed_mode_para = compute_mode_parameter(dummy_trajs_statistic)
    return speed_mode_para


def fit_velocity_profile(time_steps, velocity):
    data_length = len(velocity)
    V_max_est = np.max(velocity)
    # initial_guess = [200, 20, 80, 20, 100, V_max_est * 1.1, 0]
    bounds = [(0, data_length * 0.8), (1, data_length * 0.05), (20, data_length * 0.5), (1, data_length * 0.05),
              (1, data_length * 0.5), (V_max_est * 0.6, V_max_est * 1.2)]
    # result = minimize(objective, initial_guess, args=(time_steps, velocity)) # , bounds=bounds
    result = differential_evolution(objective, bounds, args=(time_steps, velocity))
    return result.x


def objective(params, t, velocity):
    return np.sum((velocity - trapezoid_model(t, params)) ** 2)


def trapezoid_model(t, params):
    t_start, t_r, t_h, t_f, t_l, V_max = params
    V = np.zeros_like(t, dtype=float)
    # Define velocity profile
    idx1 = (t >= t_start) & (t < t_start + t_r)
    idx2 = (t >= t_start + t_r) & (t < t_start + t_r + t_h)
    idx3 = (t >= t_start + t_r + t_h) & (t < t_start + t_r + t_h + t_f)
    idx4 = (t >= t_start + t_r + t_h + t_f)
    V[idx1] = np.interp(t[idx1], [t_start, t_start + t_r], [0, V_max])
    V[idx2] = V_max
    V[idx3] = np.interp(t[idx3], [t_start + t_r + t_h, t_start + t_r + t_h + t_f], [V_max, 0])
    V[idx4] = 0
    return V


def cluster_dummy_data(dummy_data):
    kmeans = KMeans(n_clusters=2, random_state=42)

    # Extract V_max data for clustering
    V_max = np.array(dummy_data['V_max']).reshape(-1, 1)
    kmeans.fit(V_max)

    clusters = kmeans.labels_  # Cluster labels for each V_max entry

    # Split other parameters based on the clusters
    mode_0 = {key: [] for key in dummy_data}
    mode_1 = {key: [] for key in dummy_data}

    # Assign values to clusters based on the clustering result of V_max
    for i, cluster in enumerate(clusters):
        for key in dummy_data:
            if cluster == 0:
                mode_0[key].append(dummy_data[key][i])
            else:
                mode_1[key].append(dummy_data[key][i])

    return {'mode_0': mode_0, 'mode_1': mode_1}


def remove_unusual_vmax(dummy_data, vmax_threshold):
    indices_to_remove = [i for i, vmax in enumerate(dummy_data['V_max'])
                         if vmax > vmax_threshold]

    for key in dummy_data:
        dummy_data[key] = [value for i, value in enumerate(dummy_data[key])
                           if i not in indices_to_remove]

    return dummy_data


def compute_median_acceleration(data):
    medians = {}

    for dummy, modes in data.items():
        medians[dummy] = {}

        for mode, values in modes.items():
            # Combine a_r and a_f
            all_accelerations = values['a_r'] + values['a_f']

            # Calculate the median of all accelerations for this dummy
            medians[dummy][mode] = np.median(all_accelerations)

    return medians


def compute_mode_parameter(data):
    speed_mode_para = {}

    for dummy, modes in data.items():
        speed_mode_para[dummy] = {}

        for mode, values in modes.items():
            speed_mode_para[dummy][mode] = {}

            # Combine a_r and a_f, select the median (unit transformation)
            all_accelerations = values['a_r'] + values['a_f']
            speed_mode_para[dummy][mode]['a'] = np.median(all_accelerations) * 10

            # v_max average
            speed_mode_para[dummy][mode]['V_max'] = np.average(values['V_max'])

            # Calculate t_a
            speed_mode_para[dummy][mode]['t_a'] = \
                speed_mode_para[dummy][mode]['V_max'] / speed_mode_para[dummy][mode]['a']

    return speed_mode_para


if __name__ == "__main__":
    with open('./processed_scenarios/info_all.pkl', 'rb') as file:
        info_all = pickle.load(file)

    speed_mode_para = speed_profile_analysis(info_all)

    output_path = './processed_scenarios'
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f'speed_mode_para.pkl')
    with open(output_file, 'wb') as f:
        pickle.dump(speed_mode_para, f)
