import numpy as np
import torch
from scipy.interpolate import interp1d


def to_numpy(tensor):
    """
    Convert torch tensor to numpy array, or return as-is if already numpy.
    
    Args:
        tensor: torch.Tensor or numpy array
    
    Returns:
        numpy array
    """
    if isinstance(tensor, torch.Tensor):
        return tensor.numpy()
    elif isinstance(tensor, np.ndarray):
        return tensor
    elif isinstance(tensor, list):
        return np.array(tensor)
    else:
        return tensor


def get_polyline_dir(polyline):
    """
    Calculate direction (heading) for each point in a polyline.
    
    Args:
        polyline: numpy array of shape [N, 2] with x, y coordinates
    
    Returns:
        polyline_dir: numpy array of shape [N, 1] with heading angles
    """
    polyline_dir = np.zeros((polyline.shape[0], 1))
    
    for i in range(polyline.shape[0] - 1):
        dir_vec = polyline[i + 1] - polyline[i]
        polyline_dir[i] = np.arctan2(dir_vec[1], dir_vec[0])
    
    # Use second-to-last direction for last point
    polyline_dir[-1] = polyline_dir[-2]
    
    return polyline_dir


def wrap_angle(angle):
    """
    Wrap angle to [-pi, pi] range.
    
    Args:
        angle: angle in radians
    
    Returns:
        wrapped angle in [-pi, pi]
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi


def transform_to_center_frame(center, objects, map_info):
    """
    Transform objects and map to center agent's coordinate frame.
    
    Args:
        center: array of shape [6] with [x, y, heading, vx, vy, type] of center agent
        objects: array of shape [N, T, 6] with agent trajectories
        map_info: array of shape [M, W, 4] with map polylines
    
    Returns:
        transformed_objects: array of shape [N, T, 6] in center frame
        transformed_maps: array of shape [M, W, 4] in center frame
    """
    x, y, h = center[0], center[1], center[2]
    
    transformed_objects = objects.copy()
    transformed_maps = map_info.copy()
    
    # Transform object positions
    objects_x = (objects[:, :, 0] - x) * np.cos(-h) - (objects[:, :, 1] - y) * np.sin(-h)
    objects_y = (objects[:, :, 0] - x) * np.sin(-h) + (objects[:, :, 1] - y) * np.cos(-h)
    objects_h = wrap_angle(objects[:, :, 2] - h)
    
    # Transform object velocities
    objects_vx = objects[:, :, 3] * np.cos(-h) - objects[:, :, 4] * np.sin(-h)
    objects_vy = objects[:, :, 3] * np.sin(-h) + objects[:, :, 4] * np.cos(-h)
    
    transformed_objects[:, :, 0] = objects_x
    transformed_objects[:, :, 1] = objects_y
    transformed_objects[:, :, 2] = objects_h
    transformed_objects[:, :, 3] = objects_vx
    transformed_objects[:, :, 4] = objects_vy
    
    # Zero out invalid entries
    transformed_objects[objects == 0] = 0
    
    # Transform map points
    maps_x = (map_info[:, :, 0] - x) * np.cos(-h) - (map_info[:, :, 1] - y) * np.sin(-h)
    maps_y = (map_info[:, :, 0] - x) * np.sin(-h) + (map_info[:, :, 1] - y) * np.cos(-h)
    maps_h = wrap_angle(map_info[:, :, 2] - h)
    
    transformed_maps[:, :, 0] = maps_x
    transformed_maps[:, :, 1] = maps_y
    transformed_maps[:, :, 2] = maps_h
    
    # Zero out invalid entries
    transformed_maps[map_info == 0] = 0
    
    return transformed_objects, transformed_maps


def transform_to_center_frame_no_rotation(center, objects):
    """
    Transform objects to center agent's coordinate frame without rotating headings.
    Used for future trajectories where we only need x, y positions.
    
    Args:
        center: array of shape [6] with [x, y, heading, vx, vy, type] of center agent
        objects: array of shape [N, T, 2] with future positions
    
    Returns:
        transformed_objects: array of shape [N, T, 2] in center frame
    """
    x, y, h = center[0], center[1], center[2]
    
    transformed_objects = objects.copy()
    
    # Transform positions
    objects_x = (objects[:, :, 0] - x) * np.cos(-h) - (objects[:, :, 1] - y) * np.sin(-h)
    objects_y = (objects[:, :, 0] - x) * np.sin(-h) + (objects[:, :, 1] - y) * np.cos(-h)
    
    transformed_objects[:, :, 0] = objects_x
    transformed_objects[:, :, 1] = objects_y
    
    # Zero out invalid entries
    transformed_objects[objects == 0] = 0
    
    return transformed_objects


def interpolate_trajectory(traj, kind='linear'):
    """
    Interpolate missing values in trajectory.
    
    Args:
        traj: numpy array of shape [T, 2] with x, y coordinates (may contain NaN)
        kind: interpolation method ('linear', 'cubic', etc.)
    
    Returns:
        interpolated trajectory of shape [T, 2]
    """
    valid_mask = np.isfinite(traj[:, 0])
    
    if np.sum(valid_mask) < 2:
        # Not enough points to interpolate
        return traj
    
    valid_indices = np.where(valid_mask)[0]
    valid_traj = traj[valid_mask]
    
    # Interpolate x and y separately
    f_x = interp1d(valid_indices, valid_traj[:, 0], kind=kind, 
                   bounds_error=False, fill_value='extrapolate')
    f_y = interp1d(valid_indices, valid_traj[:, 1], kind=kind, 
                   bounds_error=False, fill_value='extrapolate')
    
    all_indices = np.arange(len(traj))
    interpolated_traj = traj.copy()
    interpolated_traj[:, 0] = f_x(all_indices)
    interpolated_traj[:, 1] = f_y(all_indices)
    
    return interpolated_traj


def smooth_trajectory(traj, window_length=11, polyorder=3):
    """
    Smooth trajectory using Savitzky-Golay filter.
    
    Args:
        traj: numpy array of shape [T, 2] with x, y coordinates
        window_length: length of filter window (must be odd)
        polyorder: order of polynomial fit
    
    Returns:
        smoothed trajectory of shape [T, 2]
    """
    from scipy.signal import savgol_filter
    
    if len(traj) < window_length:
        return traj
    
    # Make sure window_length is odd and not larger than trajectory length
    window_length = min(window_length, len(traj))
    if window_length % 2 == 0:
        window_length -= 1
    
    polyorder = min(polyorder, window_length - 1)
    
    smoothed_traj = traj.copy()
    smoothed_traj[:, 0] = savgol_filter(traj[:, 0], window_length, polyorder)
    smoothed_traj[:, 1] = savgol_filter(traj[:, 1], window_length, polyorder)
    
    return smoothed_traj


def calculate_heading(traj):
    """
    Calculate heading angles from trajectory positions.
    
    Args:
        traj: numpy array of shape [T, 2] with x, y coordinates
    
    Returns:
        heading: numpy array of shape [T] with heading angles in radians
    """
    heading = np.zeros(len(traj))
    
    for i in range(len(traj) - 1):
        dx = traj[i + 1, 0] - traj[i, 0]
        dy = traj[i + 1, 1] - traj[i, 1]
        heading[i] = np.arctan2(dy, dx)
    
    # Use second-to-last heading for last point
    if len(traj) > 1:
        heading[-1] = heading[-2]
    
    return heading


def calculate_velocity(traj, dt=0.1):
    """
    Calculate velocities from trajectory positions.
    
    Args:
        traj: numpy array of shape [T, 2] with x, y coordinates
        dt: time step in seconds (default 0.1 for 10Hz)
    
    Returns:
        velocity: numpy array of shape [T, 2] with vx, vy velocities
    """
    velocity = np.zeros((len(traj), 2))
    
    for i in range(len(traj) - 1):
        velocity[i, 0] = (traj[i + 1, 0] - traj[i, 0]) / dt  # vx
        velocity[i, 1] = (traj[i + 1, 1] - traj[i, 1]) / dt  # vy
    
    # Use second-to-last velocity for last point
    if len(traj) > 1:
        velocity[-1] = velocity[-2]
    
    return velocity


def get_object_keygroups(df):
    """
    Group columns in CSV based on each object (for legacy CSV format).
    This function is kept for compatibility but not used in Waymo processing.
    
    Args:
        df: pandas DataFrame with object columns
    
    Returns:
        groups: dict mapping object keys to column lists
    """
    groups = {}
    current_group = []
    current_key = 'Timestamp'
    
    for col in df.columns:
        if 'xctr' in col:  # Each group starts with 'xctr'
            if current_group:
                groups[current_key] = current_group
            
            current_key = col
            current_group = [col]
        else:
            current_group.append(col)
    
    # Add the last group
    if current_group:
        groups[current_key] = current_group
    
    # Remove timestamp group
    if 'Timestamp' in groups:
        groups.pop('Timestamp')
    
    return groups


def visualize_scenario(hist_trajs, hist_valid, fut_trajs, fut_valid, maps, 
                      title="Scenario Visualization", save_path=None):
    """
    Visualize a processed scenario with agent trajectories and map.
    
    Args:
        hist_trajs: array of shape [N, T, 6] with history trajectories
        hist_valid: array of shape [N, T] with history validity mask
        fut_trajs: array of shape [N, T, 2] with future trajectories
        fut_valid: array of shape [N, T] with future validity mask
        maps: array of shape [M, W, 4] with map polylines
        title: plot title
        save_path: optional path to save figure
    """
    import matplotlib.pyplot as plt
    
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Plot map polylines
    for k in range(maps.shape[0]):
        valid_points = maps[k, :, 0] != 0
        if np.any(valid_points):
            ax.plot(maps[k, valid_points, 0], maps[k, valid_points, 1], 
                   'k-', linewidth=1, alpha=0.5)
    
    # Plot agent trajectories
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    
    for i in range(hist_trajs.shape[0]):
        if np.any(hist_valid[i] > 0):
            color = colors[i % len(colors)]
            
            # Plot history
            valid_hist = hist_valid[i].astype(bool)
            if np.any(valid_hist):
                ax.plot(hist_trajs[i, valid_hist, 0], hist_trajs[i, valid_hist, 1],
                       'o-', color=color, linewidth=2, markersize=4, 
                       label=f'Agent {i} (history)', alpha=0.7)
            
            # Plot future
            valid_fut = fut_valid[i].astype(bool)
            if np.any(valid_fut):
                ax.plot(fut_trajs[i, valid_fut, 0], fut_trajs[i, valid_fut, 1],
                       '--', color=color, linewidth=2, 
                       label=f'Agent {i} (future)', alpha=0.5)
    
    ax.axis('equal')
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    else:
        plt.show()
    
    plt.close()


def compute_scenario_statistics(processed_data_path):
    """
    Compute statistics from processed scenarios.
    
    Args:
        processed_data_path: path to directory with processed .pkl files
    
    Returns:
        stats: dict with statistics
    """
    import glob
    import pickle
    
    pkl_files = glob.glob(os.path.join(processed_data_path, "*.pkl"))
    
    num_agents_list = []
    valid_history_list = []
    valid_future_list = []
    num_map_polylines_list = []
    
    for pkl_file in pkl_files[:1000]:  # Sample first 1000 files
        with open(pkl_file, 'rb') as f:
            data = pickle.load(f)
        
        hist_valid = data['hist_valid']
        fut_valid = data['fut_valid']
        maps = data['maps']
        
        # Count agents with valid data
        num_agents = np.sum(np.any(hist_valid > 0, axis=1))
        num_agents_list.append(num_agents)
        
        # Average valid history/future per agent
        for i in range(hist_valid.shape[0]):
            if np.any(hist_valid[i] > 0):
                valid_history_list.append(np.mean(hist_valid[i]))
                valid_future_list.append(np.mean(fut_valid[i]))
        
        # Count map polylines
        num_map_polylines_list.append(maps.shape[0])
    
    stats = {
        'num_scenarios': len(pkl_files),
        'avg_agents_per_scenario': np.mean(num_agents_list),
        'avg_valid_history_ratio': np.mean(valid_history_list),
        'avg_valid_future_ratio': np.mean(valid_future_list),
        'avg_map_polylines': np.mean(num_map_polylines_list),
    }
    
    return stats