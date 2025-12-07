import glob
import os
import pickle
import numpy as np
import torch
from tqdm import tqdm
from matplotlib import pyplot as plt
from data_utils_waymo import *


# ==================== Configuration ====================
# Waymo data paths - UPDATE THESE TO YOUR SERVER PATHS
training_prefix = "/data2/dataset/waymo/scenario_processed/training"
validation_prefix = "/data2/dataset/waymo/scenario_processed/validation"
testing_prefix = "/data2/dataset/waymo/scenario_processed/testing"

# Output paths for processed data
output_path_training = '/data/robert/CP-X-Prediction/QCNet/data/training_processed'
output_path_validation = '/data/robert/CP-X-Prediction/QCNet/data/validation_processed'
output_path_testing = '/data/robert/CP-X-Prediction/QCNet/data/testing_processed'

os.makedirs(output_path_training, exist_ok=True)
os.makedirs(output_path_validation, exist_ok=True)
os.makedirs(output_path_testing, exist_ok=True)

# Get file lists
train_files = sorted(glob.glob(os.path.join(training_prefix, "*.pkl")))
validation_files = sorted(glob.glob(os.path.join(validation_prefix, "*.pkl")))
testing_files = sorted(glob.glob(os.path.join(testing_prefix, "*.pkl")))

# ==================== Object Types ====================
# Waymo object types (simplified from 22 subclasses to 4 main types)
object_type_class = {
    0: 'Vehicle',       # TYPE_VEHICLE
    1: 'Pedestrian',    # TYPE_PEDESTRIAN
    2: 'Cyclist',       # TYPE_CYCLIST
    3: 'Other'          # TYPE_OTHER
}

vehicle_class = ['Vehicle']
pedestrian_class = ['Pedestrian']
cyclist_class = ['Cyclist']

# Create subclass_values for indexing
subclass_values = list(object_type_class.values())

# ==================== Parameters ====================
history_timesteps = 11  # 10 past frames + 1 current frame (1.1s at 10Hz)
future_timesteps = 80   # 8s future (at 10Hz)
interval = 1  # Process every frame (set to 2 to skip frames like original code)


# ==================== Processing Functions ====================

def extract_agent_data_from_waymo(raw_data):
    """
    Extract agent trajectory data from Waymo pickle format.
    
    Args:
        raw_data: dict containing Waymo scenario data with 'agent' key
    
    Returns:
        trajectory_data: dict mapping agent_idx -> {traj, valid, sub_class}
        future_gt_data: dict mapping agent_idx -> {traj, valid}
    """
    agent_data = raw_data['agent']
    num_agents = agent_data['num_nodes']
    
    # Convert torch tensors to numpy arrays
    position = to_numpy(agent_data['position'])
    heading = to_numpy(agent_data['heading'])
    velocity = to_numpy(agent_data['velocity'])
    agent_type = to_numpy(agent_data['type'])
    valid_mask = to_numpy(agent_data['valid_mask'])
    predict_mask = to_numpy(agent_data['predict_mask'])
    
    # Initialize trajectory arrays
    hist_trajs_uncentered = np.zeros((num_agents, history_timesteps, 6), dtype=np.float32)
    hist_valid = np.zeros((num_agents, history_timesteps), dtype=np.float32)
    fut_trajs_uncentered = np.zeros((num_agents, future_timesteps, 2), dtype=np.float32)
    fut_valid = np.zeros((num_agents, future_timesteps), dtype=np.float32)
    
    # Fill in history trajectories (timesteps 0-10)
    hist_trajs_uncentered[:, :, 0:2] = position[:num_agents, :history_timesteps, :2]  # x, y
    hist_trajs_uncentered[:, :, 2] = heading[:num_agents, :history_timesteps]  # heading
    hist_trajs_uncentered[:, :, 3:5] = velocity[:num_agents, :history_timesteps, :2]  # v_x, v_y
    hist_trajs_uncentered[:, :, 5] = agent_type[:num_agents, np.newaxis]  # type (broadcast)
    hist_valid[:] = valid_mask[:num_agents, :history_timesteps]
    
    # Fill in future trajectories (timesteps 11-90)
    fut_trajs_uncentered[:, :, 0:2] = position[:num_agents, history_timesteps:history_timesteps+future_timesteps, :2]
    fut_valid[:] = predict_mask[:num_agents, history_timesteps:history_timesteps+future_timesteps]
    
    # Create trajectory_data dict
    trajectory_data = {}
    future_gt_data = {}
    
    for j in range(num_agents):
        agent_type_idx = int(agent_type[j])
        sub_class = object_type_class.get(agent_type_idx, 'Other')
        
        trajectory_data[j] = {
            'traj': hist_trajs_uncentered[j],
            'valid': hist_valid[j],
            'sub_class': sub_class
        }
        
        future_gt_data[j] = {
            'traj': fut_trajs_uncentered[j],
            'valid': fut_valid[j]
        }
    
    return trajectory_data, future_gt_data


def build_map_from_waymo(raw_data):
    """
    Build map polylines from Waymo data structure.
    
    Args:
        raw_data: dict containing 'map_polygon', 'map_point', and edge data
    
    Returns:
        map_polylines: numpy array of shape [M, W, 4] where M is number of polylines,
                      W is points per polyline, 4 is [x, y, dir, type]
    """
    map_polygon_data = raw_data['map_polygon']
    map_point_data = raw_data['map_point']
    map_point_to_polygon_data = raw_data[('map_point', 'to', 'map_polygon')]
    
    # Extract data and convert to numpy
    num_polygons = map_polygon_data['num_nodes']
    polygon_types = to_numpy(map_polygon_data['type'])
    positions = to_numpy(map_point_data['position'])
    point_types = to_numpy(map_point_data['type'])
    edge_index = to_numpy(map_point_to_polygon_data['edge_index'])
    
    # Group points by polygon
    polygon_to_points = {}
    for point_idx, polygon_idx in zip(edge_index[0], edge_index[1]):
        if polygon_idx not in polygon_to_points:
            polygon_to_points[polygon_idx] = []
        polygon_to_points[polygon_idx].append(point_idx)
    
    # Build polylines
    polylines = []
    points_per_segment = 10
    
    for polygon_idx in range(num_polygons):
        if polygon_idx not in polygon_to_points:
            continue
        
        point_indices = sorted(polygon_to_points[polygon_idx])
        polygon_type = polygon_types[polygon_idx]
        
        # Get points for this polygon
        polygon_points = positions[point_indices]
        
        if len(polygon_points) < 2:
            continue
        
        # Map Waymo polygon types to our types
        # 0: Lane, 1: Stop sign, 2: Speed bump, 3: Crosswalk, etc.
        if polygon_type == 0:  # Lane
            global_type = 1
        elif polygon_type == 3:  # Crosswalk
            global_type = 3
        else:
            global_type = 0  # Other
        
        # Create polyline with type
        polyline = np.zeros((len(polygon_points), 4), dtype=np.float32)
        polyline[:, 0:2] = polygon_points[:, 0:2]  # x, y
        polyline[:, 3] = global_type  # type
        
        # Calculate direction for each point
        polyline_dir = get_polyline_dir(polyline[:, 0:2])
        polyline[:, 2] = polyline_dir.squeeze()
        
        # Split long polylines into segments
        if len(polygon_points) > points_per_segment:
            for i in range(0, len(polygon_points), points_per_segment):
                segment = polyline[i:i+points_per_segment]
                
                # Filter by distance (keep polylines within 50m)
                d = np.linalg.norm(segment[:, 0:2], axis=-1)
                if np.max(d) > 50:
                    continue
                
                # Skip very short segments
                if segment.shape[0] < 5:
                    continue
                
                # Pad if needed
                if segment.shape[0] < points_per_segment:
                    padding = np.zeros((points_per_segment - segment.shape[0], 4), dtype=np.float32)
                    segment = np.concatenate([segment, padding], axis=0)
                
                polylines.append(segment)
        else:
            # Keep short polylines as-is if they're valid
            if len(polygon_points) >= 5:
                d = np.linalg.norm(polyline[:, 0:2], axis=-1)
                if np.max(d) <= 50:
                    polylines.append(polyline)
    
    if len(polylines) == 0:
        # Return empty map with proper shape
        return np.zeros((1, points_per_segment, 4), dtype=np.float32)
    
    map_polylines = np.array(polylines, dtype=np.float32)
    return map_polylines


def process_model_input(trajectory_data, center_idx, map_data, future_data, debug=False):
    """
    Process raw trajectory and map data into model input format.
    
    Args:
        trajectory_data: dict of agent trajectories
        center_idx: index of the center agent
        map_data: map polylines
        future_data: future ground truth trajectories
        debug: whether to visualize
    
    Returns:
        inputs: dict with keys ['hist_trajs', 'maps', 'fut_gt_trajs', 'hist_valid', 'fut_valid']
    """
    # Get center agent state
    center_object_state = trajectory_data[center_idx]['traj'][-1]
    
    # Stack all agent trajectories
    object_trajs = np.stack([v['traj'][-history_timesteps:] for k, v in trajectory_data.items()], axis=0)
    
    # Transform to center frame
    objects, map_polyline = transform_to_center_frame(center_object_state, object_trajs, map_data)
    
    # Transform future trajectories
    future_trajs = np.stack([v['traj'] for k, v in future_data.items()], axis=0)
    objects_future = transform_to_center_frame_no_rotation(center_object_state, future_trajs)
    
    # Put center object at the first index
    order = list(range(objects.shape[0]))
    order[0], order[center_idx] = order[center_idx], order[0]
    
    # Initialize arrays (max 5 agents)
    num_agents = 5
    hist_trajs = np.zeros((num_agents, history_timesteps, 6), dtype=np.float32)
    hist_valid = np.zeros((num_agents, history_timesteps), dtype=np.float32)
    fut_trajs = np.zeros((num_agents, future_timesteps, 2), dtype=np.float32)
    fut_valid = np.zeros((num_agents, future_timesteps), dtype=np.float32)
    
    # Fill in data for up to 5 agents
    for i, idx in enumerate(order):
        if i >= num_agents:
            break
        
        traj = objects[idx]
        valid = trajectory_data[list(trajectory_data.keys())[idx]]['valid'][-history_timesteps:]
        sub_class = trajectory_data[list(trajectory_data.keys())[idx]]['sub_class']
        
        # Get type index
        type_idx = subclass_values.index(sub_class) if sub_class in subclass_values else 0
        
        hist_trajs[i, :, :5] = traj[:, :5]
        hist_trajs[i, :, 5] = float(type_idx)
        hist_valid[i, :] = valid
        
        future_traj = objects_future[idx]
        valid_fut = future_data[list(future_data.keys())[idx]]['valid']
        fut_trajs[i, :, :] = future_traj
        fut_valid[i, :] = valid_fut
    
    inputs = {
        'hist_trajs': hist_trajs,
        'maps': map_polyline,
        'fut_gt_trajs': fut_trajs,
        'hist_valid': hist_valid,
        'fut_valid': fut_valid
    }
    
    # Visualization for debugging
    if debug:
        plt.figure(figsize=(10, 10))
        for k in range(map_polyline.shape[0]):
            plt.plot(map_polyline[k, :, 0], map_polyline[k, :, 1], 'k--', linewidth=2)
        
        for k in range(hist_trajs.shape[0]):
            plt.scatter(hist_trajs[k, :, 0], hist_trajs[k, :, 1], s=100, label=f'Agent {k}')
        
        for k in range(fut_trajs.shape[0]):
            plt.plot(fut_trajs[k, :, 0], fut_trajs[k, :, 1], 'r--', linewidth=2)
        
        plt.axis('equal')
        plt.legend()
        plt.title('Transformed to Center Frame')
        plt.show()
    
    return inputs


# ==================== Main Processing ====================

if __name__ == '__main__':
    import logging
    import sys
    from datetime import datetime
    
    # Setup logging
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"process_waymo_qcnet_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.info("=== QCNet Waymo data processing started ===")
    logging.info(f"PID: {os.getpid()}")
    logging.info(f"Logging to: {log_file}")
    
    # Process each dataset split
    all_datasets = {
        'training': (train_files, output_path_training),
        'validation': (validation_files, output_path_validation),
        'testing': (testing_files, output_path_testing)
    }
    
    for split_name, (input_files, output_path) in all_datasets.items():
        logging.info(f"\n{'='*60}")
        logging.info(f"Processing {split_name} split: {len(input_files)} files")
        logging.info(f"{'='*60}")
        
        processed_count = 0
        skipped_count = 0
        
        for i in tqdm(range(len(input_files)), desc=f"Processing {split_name}"):
            try:
                # Load Waymo scenario
                with open(input_files[i], 'rb') as f:
                    raw_data = pickle.load(f)
                
                scenario_id = raw_data['scenario_id']
                
                # Extract agent trajectories and future GT
                trajectory_data, future_gt_data = extract_agent_data_from_waymo(raw_data)
                num_agents = len(trajectory_data)
                
                # Build map polylines
                map_polyline = build_map_from_waymo(raw_data)
                
                # Get agent IDs
                agent_ids = to_numpy(raw_data['agent']['id'])
                
                # Process each agent as center agent
                for ki in range(num_agents):
                    agent_id = int(agent_ids[ki])
                    agent_trajectory_data = trajectory_data[ki]
                    
                    # Check if agent has enough valid history
                    # Require at least 10 out of 11 history timesteps to be valid
                    valid_history = np.sum(agent_trajectory_data['valid'][:history_timesteps])
                    
                    if valid_history < (history_timesteps - 1):
                        skipped_count += 1
                        continue
                    
                    # Process this agent as center
                    inputs = process_model_input(trajectory_data, ki, map_polyline, future_gt_data)
                    
                    # Save processed data
                    output_file = os.path.join(output_path, f"{scenario_id}_{agent_id}.pkl")
                    with open(output_file, 'wb') as f:
                        pickle.dump(inputs, f)
                    
                    processed_count += 1
                    
                    # Data augmentation: duplicate vehicle data
                    if agent_trajectory_data['sub_class'] in vehicle_class:
                        for d in range(5):
                            # Process again (could add small perturbations here)
                            inputs = process_model_input(trajectory_data, ki, map_polyline, future_gt_data)
                            output_file = os.path.join(output_path, f"{scenario_id}_{agent_id}_{d+1}.pkl")
                            with open(output_file, 'wb') as f:
                                pickle.dump(inputs, f)
                            processed_count += 1
                
                if (i + 1) % 100 == 0:
                    logging.info(f"Processed {i+1}/{len(input_files)} scenarios. "
                               f"Total samples: {processed_count}, Skipped: {skipped_count}")
                    
            except Exception as e:
                logging.exception(f"Error processing file {input_files[i]}: {e}")
                continue
        
        logging.info(f"\n{split_name.upper()} Summary:")
        logging.info(f"  Scenarios processed: {len(input_files)}")
        logging.info(f"  Samples created: {processed_count}")
        logging.info(f"  Samples skipped: {skipped_count}")
    
    logging.info("\n=== Processing complete ===")