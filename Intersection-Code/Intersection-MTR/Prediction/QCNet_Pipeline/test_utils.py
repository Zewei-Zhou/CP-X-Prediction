import pickle
import numpy as np
import matplotlib.pyplot as plt
from map import *
from scipy.signal import savgol_filter
from scipy import interpolate


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
        dy = traj[i, 1] - traj[i-1, 1]
        dx = traj[i, 0] - traj[i-1, 0]
        heading[i] = np.arctan2(dy, dx+1e-3)

    heading[0] = heading[1]

    return heading


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
        velocity[i, 0] = (traj[i, 0] - traj[i-1, 0]) / 0.1
        velocity[i, 1] = (traj[i, 1] - traj[i-1, 1]) / 0.1
    
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

        if type[0] == 1: # centerline
            plt.plot(line[:, 0], line[:, 1], color='gray', linewidth=32, zorder=0, label='road')
        elif type[0] == 3: # crosswalk polygon
            plt.fill(line[:, 0], line[:, 1], color='xkcd:orange', alpha=0.5, zorder=3, label='crosswalk')
        elif type[0] == 2: # sidewalk
            plt.plot(line[:, 0], line[:, 1], color='lightgrey', linewidth=16, zorder=2, label='sidewalk')
        else: # boundary
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


def plot_trajectory(trajs, color='r'):
    for i, traj in enumerate(trajs):
        traj = smooth_trajectory(traj)
        plt.plot(traj[:, 0], traj[:, 1], color, linewidth=3)
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

    g_x = trajs[:, :, 0] * np.cos(center_obj_state[2]) - trajs[:, :, 1] * np.sin(center_obj_state[2]) + center_obj_state[0]
    g_y = trajs[:, :, 0] * np.sin(center_obj_state[2]) + trajs[:, :, 1] * np.cos(center_obj_state[2]) + center_obj_state[1]
    global_trajs[:, :, 0] = g_x
    global_trajs[:, :, 1] = g_y

    return global_trajs


if __name__ == '__main__':
    fig = plt.figure(figsize=(20, 20))
    plot_vector_map()
    plt.show()