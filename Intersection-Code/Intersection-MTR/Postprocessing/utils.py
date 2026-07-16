import numpy as np
from scipy.signal import savgol_filter


def check_offroad(traj, class_name, boundaries):
    """
    Check if the trajectory is off-road.

    Args:
        traj: the trajectory to check
        class_name: the class name of the object
        boundaries: the boundaries of the vector map

    Returns:
        True if the trajectory is off-road, False otherwise
    """
    if class_name != "TYPE_VEHICLE":
        return False

    for boundary in boundaries:
        if traj.intersects(boundary):
            return False

    return True


def smooth_trajectory(traj, order=5, window_length=15):
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


def velocity_calculation(traj):
    """
    Calculate the velocity of the trajectory.

    Args:
        traj: the trajectory to calculate the velocity

    Returns:
        the velocity of the trajectory
    """
    velocity = np.zeros((traj.shape[0], 2))

    for i in range(traj.shape[0] - 1):
        velocity[i, 0] = (traj[i+1, 0] - traj[i, 0]) / 0.1
        velocity[i, 1] = (traj[i+1, 1] - traj[i, 1]) / 0.1

    velocity[-1] = velocity[-2]

    return velocity


def yaw_calculation(traj):
    """
    Calculate the yaw of the trajectory.

    Args:
        traj: the trajectory to calculate the yaw

    Returns:
        the yaw of the trajectory
    """
    yaw = np.zeros((traj.shape[0], 1))

    for i in range(traj.shape[0] - 1):
        yaw[i, 0] = np.arctan2(traj[i+1, 1] - traj[i, 1], traj[i+1, 0] - traj[i, 0])

    yaw[-1, 0] = yaw[-2, 0]

    return yaw