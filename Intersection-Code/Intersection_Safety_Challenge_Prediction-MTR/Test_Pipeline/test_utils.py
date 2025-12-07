import pickle
import numpy as np
import matplotlib.pyplot as plt
from map import *
from data_utils import optimize_traj
from scipy.signal import savgol_filter
from scipy import interpolate

def object_type_to_mtr_type(sub_class):
    if 'Dummy' in sub_class:
        return 'TYPE_DUMMY'
    pedestrian_class = ['VRU_Child', 'VRU_Adult','VRU_Adult_Using_Wheelchair',\
                           'VRU_Adult_Using_Scooter_or_Skateboard', 'VRU_Other']
    cyclist_class = ['VRU_Adult_Using_Non-Motorized_Device/Prop_Other','VRU_Adult_Using_Bicycle']
    vehicle_class = ['Passenger_Vehicle', 'Vehicle_Other']

    if sub_class in pedestrian_class:
        return 'TYPE_PEDESTRIAN'
    elif sub_class in cyclist_class:
        return 'TYPE_CYCLIST'
    elif sub_class in vehicle_class:
        return 'TYPE_VEHICLE'
    else:
        print('Unknown sub_class:', sub_class)
        exit()

def calculate_heading(traj):
    """
    Calculate the heading of the trajectory.

    Args:
        traj: the trajectory

    Returns:
        the heading of the trajectory
    """
    heading = np.zeros(traj.shape[0])
    for i in range(1, traj.shape[0]):
        dy = traj[i, 1] - traj[i - 1, 1]
        dx = traj[i, 0] - traj[i - 1, 0]
        heading[i] = np.arctan2(dy, dx + 1e-3)

    heading[0] = heading[1]

    return heading

def calculate_heading_smoothed(xctr, yctr, valid, subclass):
    mtr_class = object_type_to_mtr_type(subclass)
    if mtr_class == 'TYPE_PEDESTRIAN':
        static_threshold = 0.015
        k1 = 0.0001
        k2 = 0.0001
        k3 = 1
        points_per_segment = 40
    elif mtr_class == 'TYPE_CYCLIST':
        static_threshold = 0.015
        k1 = 0.0001
        k2 = 0.0001
        k3 = 1
        points_per_segment = 40
    elif mtr_class == 'TYPE_DUMMY':
        static_threshold = 0.015
        k1 = 0.0001
        k2 = 0.0001
        k3 = 1
        points_per_segment = 40
    elif mtr_class == 'TYPE_VEHICLE':
        static_threshold = 0.1
        k1 = 0.0001
        k2 = 0.0001
        k3 = 10
        degree = 5
        points_per_segment = 20
    # filter out the static points
    valid_x = xctr[valid == 1]
    valid_y = yctr[valid == 1]
    dx = np.diff(valid_x)
    dy = np.diff(valid_y)

    static_mask = (np.abs(dx) <= static_threshold) & (np.abs(dy) <= static_threshold)
    static_start = static_mask[0]
    static_mask = np.concatenate(([static_start], static_mask))
    # Create a mask for non-static parts (static_mask is not True)
    non_static_mask = ~static_mask
    # Filter out the non-static points
    non_static_x = valid_x[non_static_mask]
    non_static_y = valid_y[non_static_mask]
    # optimize the non static points
    optimized_result = optimize_traj(non_static_x, non_static_y, k1,k2,k3,points_per_segment)
    
    # optimization failed since non static points are less than (8? need to check)
    if optimized_result is None:
        # print('Optimization failed')
        # print(csv_file)
        # print(key)
        
        # plt.scatter(valid_x[static_mask], valid_y[static_mask], color='blue', label='Static Points')
        # plt.scatter(valid_x[non_static_mask], valid_y[non_static_mask], color='orange', label='Non-static Points')

        # print("-------all static--------")
        valid_heading = np.zeros(valid_x.shape)
    else:
        x_coeff_list, y_coeff_list,closest_x_points, closest_y_points, derivative_x, derivative_y = optimized_result
    
        optimized_valid_x = np.full(valid_x.shape, np.nan)
        optimized_valid_y = np.full(valid_y.shape, np.nan)
        optimized_valid_x[non_static_mask] = closest_x_points
        optimized_valid_y[non_static_mask] = closest_y_points

        valid_heading = np.full(valid_x.shape, np.nan)
        valid_heading[non_static_mask] = np.arctan2(derivative_y, derivative_x)   

        # Fill in the static points (traj and heading), optimized_valid_x, optimized_valid_y unused now, might be deleted later
        static_indices = np.where(static_mask)[0]
        for i in static_indices:
            if i > 0:
                # Find the last non-static point before the current static point
                previous_non_static = i - 1
                while previous_non_static >= 0 and static_mask[previous_non_static]:
                    previous_non_static -= 1
                if previous_non_static >= 0:
                    optimized_valid_x[i] = optimized_valid_x[previous_non_static]
                    optimized_valid_y[i] = optimized_valid_y[previous_non_static]
                    valid_heading[i] = valid_heading[previous_non_static]

            if np.isnan(optimized_valid_x[i]):  # If no previous non-static point was found
                # Use the next non-static point if the static point is at the start or no previous found
                next_non_static = i + 1
                while next_non_static < len(static_mask) and static_mask[next_non_static]:
                    next_non_static += 1
                if next_non_static < len(static_mask):
                    optimized_valid_x[i] = optimized_valid_x[next_non_static]
                    optimized_valid_y[i] = optimized_valid_y[next_non_static]
                    valid_heading[i] = valid_heading[next_non_static]

    headings = np.zeros(len(xctr))
    headings[valid == 1] = valid_heading
    return headings
    
def get_prior_dummy_heading(run_id, valid_heading,
                            dummy_pos_dict, track_heading):
    # hard coding the path
    if not dummy_pos_dict:
        combined_dict = np.load('/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/combined_dict.npy', allow_pickle=True).item()
        dummy_pos_dict = {}
        for direction, details in combined_dict['dummy_heading_dict'].items():
            for run in details['run']:
                dummy_pos_dict[run] = direction

    if not track_heading:
        with open('/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/track_heading.pkl', 'rb') as f:
            track_heading = pickle.load(f)

    if int(run_id) in dummy_pos_dict:
        track_pos = dummy_pos_dict[int(run_id)].split('_')[0]
        track_direction = dummy_pos_dict[int(run_id)].split('_')[-1]
        heading = track_heading[int(track_pos)][int(track_direction)]
        valid_heading[:] = heading

    return valid_heading


def calculate_velocity(traj):
    """
    Calculate the velocity of the trajectory.

    Args:
        traj: the trajectory

    Returns:
        the velocity of the trajectory
    """
    velocity = np.zeros(traj.shape)
    for i in range(1, traj.shape[0]):
        velocity[i, 0] = (traj[i, 0] - traj[i - 1, 0]) / 0.1
        velocity[i, 1] = (traj[i, 1] - traj[i - 1, 1]) / 0.1

    velocity[0] = velocity[1]

    return velocity


def interpolate_trajectory(traj):
    """
    Interpolate the trajectory for missing timesteps.
    Only works for missing timesteps in the middle of the trajectory.
    
    Args:
        traj: the trajectory to interpolate
    
    Returns:
        the interpolated trajectory
    """
    inds = np.arange(traj.shape[0])
    good = np.where(np.isfinite(traj[:, 0]))[0]
    x, y = traj[:, 0], traj[:, 1]
    f_x = interpolate.interp1d(inds[good], x[good], bounds_error=False)
    f_y = interpolate.interp1d(inds[good], y[good], bounds_error=False)
    new_x = f_x(inds)
    new_y = f_y(inds)
    new_traj = np.stack([new_x, new_y], axis=1)

    return new_traj


def plot_map(map):
    for i in range(map.shape[0]):
        type = map[i, :, 3]
        line = map[i][type != 0]

        if type[0] == 1:  # centerline
            plt.plot(line[:, 0], line[:, 1], color='gray', linewidth=32, zorder=0, label='road')
        elif type[0] == 3:  # crosswalk polygon
            plt.fill(line[:, 0], line[:, 1], color='xkcd:orange', alpha=0.5, zorder=3, label='crosswalk')
        elif type[0] == 2:  # sidewalk
            plt.plot(line[:, 0], line[:, 1], color='lightgrey', linewidth=16, zorder=2, label='sidewalk')
        else:  # boundary
            plt.plot(line[:, 0], line[:, 1], 'k--', linewidth=2, zorder=1, label='boundary')


def plot_agent(pos, sub_class, color='r'):
    plt.scatter(pos[0], pos[1], color=color, s=100, zorder=4)
    plt.text(pos[0], pos[1], sub_class, fontsize=12, color='black', zorder=5)


def plot_vector_map():
    with open('vector_map.pkl', 'rb') as file:
        map = pickle.load(file)
        map_features = map.map_features

    for feature in map_features:
        if isinstance(feature, Lane):
            if feature.type == LaneType.Driving:
                centerline = np.array([[p.x, p.y] for p in feature.polyline])
                plt.plot(centerline[:, 0], centerline[:, 1], color='gray', linewidth=32, zorder=0)
                boundary = np.array([[p.x, p.y] for p in feature.boundary])
                plt.plot(boundary[:, 0], boundary[:, 1], 'k--', linewidth=2, zorder=1)

            elif feature.type == LaneType.Sidewalk:
                centerline = np.array([[p.x, p.y] for p in feature.polyline])
                plt.plot(centerline[:, 0], centerline[:, 1], color='lightgrey', linewidth=16, zorder=2)

        elif isinstance(feature, Crosswalk):
            line = np.array([[p.x, p.y] for p in feature.polygon])
            plt.fill(line[:, 0], line[:, 1], color='xkcd:orange', alpha=0.5, zorder=3)


def plot_trajectory(trajs, color='r', history=False):
    if history:
        plt.plot(trajs[:, 0], trajs[:, 1], color=color, linestyle='dashed', linewidth=5)
    else:
        for i, traj in enumerate(trajs):
            plt.plot(traj[:, 0], traj[:, 1], color, linewidth=4)
            plt.text(traj[-1, 0], traj[-1, 1], str(i), fontsize=20, color='black', zorder=5)


def smooth_trajectory(traj, order=5, window_length=21):
    """
    Smooth the trajectory using a Savitzky-Golay filter.

    Args:
        traj: the trajectory to smooth
        order: the order of the filter

    Returns:
        the smoothed trajectory
    """
    traj[:, 0] = savgol_filter(traj[:, 0], window_length=window_length, polyorder=order)
    traj[:, 1] = savgol_filter(traj[:, 1], window_length=window_length, polyorder=order)

    return traj


def transformer_to_global_frame(trajs, center_obj_state):
    """
    Transform the trajectories to the global frame.

    Args:
        trajs: the trajectories to transform
        center_obj_state: the state of the center object

    Returns:
        the transformed trajectories
    """
    global_trajs = np.zeros_like(trajs)

    g_x = trajs[:, :, 0] * np.cos(center_obj_state[2]) - trajs[:, :, 1] * np.sin(center_obj_state[2]) + \
          center_obj_state[0]
    g_y = trajs[:, :, 0] * np.sin(center_obj_state[2]) + trajs[:, :, 1] * np.cos(center_obj_state[2]) + \
          center_obj_state[1]
    global_trajs[:, :, 0] = g_x
    global_trajs[:, :, 1] = g_y

    return global_trajs


if __name__ == '__main__':
    fig = plt.figure(figsize=(20, 20))
    plot_vector_map()
    plt.show()
