# Info on the Waymo Open Motion Dataset structure 
"""
Loaded object type: <class 'dict'>
Length (len()): 7
Number of keys: 7
First 20 keys (repr) and types:
0: type=str, repr='scenario_id'
1: type=str, repr='city'
2: type=str, repr='agent'
3: type=str, repr='map_polygon'
4: type=str, repr='map_point'
5: type=tuple, repr=('map_point', 'to', 'map_polygon')
6: type=tuple, repr=('map_polygon', 'to', 'map_polygon')
"""
"""
Loaded type: <class 'dict'>
key='scenario_id'                                                                                                             type=str                   len=16
key='city'                                                                                                                    type=float64               len=None
key='agent'                                                                                                                   type=dict                  len=11
key='map_polygon'                                                                                                             type=dict                  len=3
key='map_point'                                                                                                               type=dict                  len=6
key=('map_point', 'to', 'map_polygon')                                                                                        type=dict                  len=1
key=('map_polygon', 'to', 'map_polygon')                                                                                      type=dict                  len=2
"""

# Need to go from what the data looks like above to what the model needs below

# Info on the old data structure used for training in intersection challenge
"""
 # fill in array
    hist_trajs = np.zeros((5, history_timesteps, 6), dtype=np.float32) # x, y, heading, v_x, v_y, type
    hist_valid = np.zeros((5, history_timesteps), dtype=np.float32)
    fut_trajs = np.zeros((5, future_timesteps, 2), dtype=np.float32)
    fut_valid = np.zeros((5, future_timesteps), dtype=np.float32)
"""

"""
  inputs = {'hist_trajs': hist_trajs, 'maps': map_polyline, 'fut_gt_trajs': fut_trajs,
              'hist_valid': hist_valid, 'fut_valid': fut_valid}
"""

"""
{
    'hist_trajs': (5, 11, 6),     # 5 agents, 11 timesteps, [x,y,heading,vx,vy,type]
    'hist_valid': (5, 11),         # Valid timestep mask
    'fut_gt_trajs': (5, 80, 2),   # Future trajectories [x, y]
    'fut_valid': (5, 80),          # Future valid mask
    'maps': map_polyline           # Road geometry
}
"""

"""
{
    'scenario_id': str,
    'city': float,
    'agent': {
        'num_nodes': 12,  # Total agents in scene
        'av_index': 11,
        'valid_mask': (12, 91),    # Which timesteps have data
        'predict_mask': (12, 91),  # Which timesteps to predict
        'position': (12, 91, 3),   # [x, y, z]
        'heading': (12, 91),
        'velocity': (12, 91, 3),   # [vx, vy, vz]
        'type': (12,),
        'category': (12,),
        'shape': (12, 91, 3)
    },
    'map_polygon': {...},
    'map_point': {...},
    ('map_point', 'to', 'map_polygon'): {...},
    ('map_polygon', 'to', 'map_polygon'): {...}
}
"""

"""
{
    'hist_trajs': (5, 11, 6),      # [x, y, heading, vx, vy, type]
    'hist_valid': (5, 11),          # History validity mask
    'fut_gt_trajs': (5, 80, 2),    # [x, y] only
    'fut_valid': (5, 80),           # Future validity mask
    'maps': map_polyline            # Simplified map
}
"""


import glob
import os
import pickle
import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from matplotlib import pyplot as plt
from test_utils import *
from data_utils import *
from maps import *

# Data
training_prefix = "/data2/dataset/waymo/scenario_processed/training" 
validation_prefix = "/data2/dataset/waymo/scenario_processed/validation"
testing_prefix = "/data2/dataset/waymo/scenario_processed/testing"
# training files are .pkl files, not .csv like before
train_files = list(glob.glob(os.path.join(training_prefix, "*.pkl")))
validation_files = list(glob.glob(os.path.join(validation_prefix, "*.pkl")))
testing_files = list(glob.glob(os.path.join(testing_prefix, "*.pkl")))

# map class
# map_class = {
#     0: 'Other',
#     1: 'Lane',
#     2: 'SideWalk',
#     3: 'CrossWalk',
#     4: 'Boundary',
# }

# At the top, fix vehicle_class (remove duplicate)
object_type_class = {
    0: 'Vehicle',       # TYPE_VEHICLE
    1: 'Pedestrian',    # TYPE_PEDESTRIAN
    2: 'Cyclist',       # TYPE_CYCLIST (or other VRU)
    3: 'Other'          # TYPE_OTHER
}

vehicle_class = ['Vehicle']  # Remove the duplicate definition

# Create subclass_values for backward compatibility
subclass_values = list(object_type_class.values())

# Parameters
output_path_training = '/data/robert/CP-X-Prediction/MTR/data/training_processed'
os.makedirs(output_path_training, exist_ok=True)

output_path_validation = '/data/robert/CP-X-Prediction/MTR/data/validation_processed'
os.makedirs(output_path_validation, exist_ok=True)

output_path_testing = '/data/robert/CP-X-Prediction/MTR/data/testing_processed'
os.makedirs(output_path_testing, exist_ok=True)

# includes pasts 10 history frames + 1 current frame
history_timesteps = 11
future_timesteps = 80
interval = 2

def process_model_input(trajectory_data, center_idx, map_data, future_data, debug=False):
    center_object_state = trajectory_data[list(trajectory_data.keys())[center_idx]]['traj'][-1]
    object_trajs = np.stack([v['traj'][-history_timesteps:] for k, v in trajectory_data.items()], axis=0)
    objects, map_polyline = transform_to_center_frame(center_object_state, object_trajs, map_data)
    future_trajs = np.stack([v['traj'] for k, v in future_data.items()], axis=0)
    objects_future = transform_to_center_frame_no_rotation(center_object_state, future_trajs)

     # put center object at the first index in order
    order = list(range(objects.shape[0]))
    order[0], order[center_idx] = order[center_idx], order[0]

    # fill in array
    hist_trajs = np.zeros((5, history_timesteps, 6), dtype=np.float32) # x, y, heading, v_x, v_y, type
    hist_valid = np.zeros((5, history_timesteps), dtype=np.float32)
    fut_trajs = np.zeros((5, future_timesteps, 2), dtype=np.float32)
    fut_valid = np.zeros((5, future_timesteps), dtype=np.float32)
    
    num_agents = 5
    for i, idx in enumerate(order):
        if i >= num_agents:
            break
        # if i >= len(trajectory_data):
        #     break

        traj = objects[idx]
        valid = trajectory_data[list(trajectory_data.keys())[idx]]['valid'][-history_timesteps:]
        sub_class = trajectory_data[list(trajectory_data.keys())[idx]]['sub_class']
        # use this index for the type 
        type_index = subclass_values.index(sub_class)
        hist_trajs[i, :, :5] = traj[:, :5]
        hist_trajs[i, :, 5] = float(type_index)
        hist_valid[i, :] = valid

        future_traj = objects_future[idx]
        valid = future_data[list(future_data.keys())[idx]]['valid']
        fut_trajs[i, :, :] = future_traj
        fut_valid[i, :] = valid
    
    inputs = {'hist_trajs': hist_trajs, 'maps': map_polyline, 'fut_gt_trajs': fut_trajs,
              'hist_valid': hist_valid, 'fut_valid': fut_valid}
    
    if debug:
        plt.figure(figsize=(10, 10))
        for k in range(map_polyline.shape[0]):
            plt.plot(map_polyline[k, :, 0], map_polyline[k, :, 1], 'k--', linewidth=2)
  
        for k in range(hist_trajs.shape[0]):
            plt.scatter(hist_trajs[k, :, 0], hist_trajs[k, :, 1], s=100, label='Agent %d' % k)
        
        for k in range(fut_trajs.shape[0]):
            plt.plot(fut_trajs[k, :, 0], fut_trajs[k, :, 1], 'r--', linewidth=2)
          
        plt.axis('equal')
        plt.show()
    
    return inputs

def decode_map_features_from_tensor_data(map_polygon_data, map_point_data, 
                                         map_point_to_polygon_data, 
                                         map_polygon_to_polygon_data):
    """
    Convert tensor-based map data to Map dataclass format.
    
    Args:
        map_polygon_data: dict with 'num_nodes', 'type', 'light_type' tensors
        map_point_data: dict with 'num_nodes', 'position', 'orientation', 'magnitude', 'height', 'type' tensors
        map_point_to_polygon_data: dict with 'edge_index' tensor
        map_polygon_to_polygon_data: dict with 'edge_index' and 'type' tensors
    
    Returns:
        Map object with map_features list
    """
    
    # Extract data
    num_polygons = map_polygon_data['num_nodes']
    polygon_types = map_polygon_data['type'].numpy() if isinstance(map_polygon_data['type'], torch.Tensor) else map_polygon_data['type']
    light_types = map_polygon_data['light_type'].numpy() if isinstance(map_polygon_data['light_type'], torch.Tensor) else map_polygon_data['light_type']
    
    positions = map_point_data['position'].numpy() if isinstance(map_point_data['position'], torch.Tensor) else map_point_data['position']
    point_types = map_point_data['type'].numpy() if isinstance(map_point_data['type'], torch.Tensor) else map_point_data['type']
    
    # edge_index: [2, num_edges], where edge_index[0] is point index, edge_index[1] is polygon index
    edge_index = map_point_to_polygon_data['edge_index'].numpy() if isinstance(map_point_to_polygon_data['edge_index'], torch.Tensor) else map_point_to_polygon_data['edge_index']
    
    # polygon_edge_index: connections between polygons
    polygon_edge_index = map_polygon_to_polygon_data['edge_index'].numpy() if isinstance(map_polygon_to_polygon_data['edge_index'], torch.Tensor) else map_polygon_to_polygon_data['edge_index']
    polygon_edge_types = map_polygon_to_polygon_data['type'].numpy() if isinstance(map_polygon_to_polygon_data['type'], torch.Tensor) else map_polygon_to_polygon_data['type']
    
    # Group points by polygon
    polygon_to_points = {}
    for point_idx, polygon_idx in zip(edge_index[0], edge_index[1]):
        if polygon_idx not in polygon_to_points:
            polygon_to_points[polygon_idx] = []
        polygon_to_points[polygon_idx].append(point_idx)
    
    # Build polygon connectivity map (entry/exit lanes)
    polygon_connections = {}  # polygon_id -> {'entry': [], 'exit': []}
    for i in range(polygon_edge_index.shape[1]):
        from_poly = polygon_edge_index[0, i]
        to_poly = polygon_edge_index[1, i]
        edge_type = polygon_edge_types[i]
        
        if from_poly not in polygon_connections:
            polygon_connections[from_poly] = {'entry': [], 'exit': []}
        if to_poly not in polygon_connections:
            polygon_connections[to_poly] = {'entry': [], 'exit': []}
        
        # Add connections (simplified - adjust based on your edge_type semantics)
        polygon_connections[from_poly]['exit'].append(str(to_poly))
        polygon_connections[to_poly]['entry'].append(str(from_poly))
    
    # Convert to map features
    map_features = []
    
    for polygon_idx in range(num_polygons):
        if polygon_idx not in polygon_to_points:
            continue
        
        point_indices = sorted(polygon_to_points[polygon_idx])
        polygon_type = polygon_types[polygon_idx]
        
        # Extract points for this polygon
        polygon_points = positions[point_indices]
        
        # Determine feature type based on polygon type
        if polygon_type == 0:  # Lane (most common type)
            # Create Lane object
            polyline = [MapPoint(x=float(p[0]), y=float(p[1])) for p in polygon_points]
            
            # Get connections
            connections = polygon_connections.get(polygon_idx, {'entry': [], 'exit': []})
            
            lane = Lane(
                road_id=polygon_idx // 10,  # Simplified road_id grouping
                lane_id=polygon_idx,
                type=LaneType.Driving,  # Default to driving lane
                polyline=polyline,
                entry_lanes=connections['entry'],
                exit_lanes=connections['exit'],
                boundary=[]  # Boundary would need additional processing
            )
            map_features.append(lane)
            
        elif polygon_type == 3:  # Crosswalk (based on your data)
            polygon = [MapPoint(x=float(p[0]), y=float(p[1])) for p in polygon_points]
            crosswalk = Crosswalk(
                polygon=polygon,
                id=polygon_idx
            )
            map_features.append(crosswalk)
    
    # Handle road lines from point types
    # Group consecutive points of same type as road lines
    road_line_points = {}
    for point_idx, point_type in enumerate(point_types):
        if point_type in [2, 4, 12, 15]:  # Types that might represent road lines
            if point_type not in road_line_points:
                road_line_points[point_type] = []
            road_line_points[point_type].append(point_idx)
    
    # Create RoadLine objects
    road_line_id = 1000
    for line_type, point_indices in road_line_points.items():
        if len(point_indices) > 2:  # Only create if we have enough points
            # Group consecutive points
            segments = []
            current_segment = [point_indices[0]]
            
            for i in range(1, len(point_indices)):
                if point_indices[i] == point_indices[i-1] + 1:
                    current_segment.append(point_indices[i])
                else:
                    if len(current_segment) >= 2:
                        segments.append(current_segment)
                    current_segment = [point_indices[i]]
            
            if len(current_segment) >= 2:
                segments.append(current_segment)
            
            # Create RoadLine for each segment
            for segment in segments[:10]:  # Limit to avoid too many road lines
                polyline = [MapPoint(x=float(positions[idx, 0]), y=float(positions[idx, 1])) 
                           for idx in segment]
                road_line = RoadLine(
                    id=road_line_id,
                    type=f"type_{line_type}",
                    polyline=polyline
                )
                map_features.append(road_line)
                road_line_id += 1
    
    return Map(map_features=map_features)


def build_map_polyline_from_pkl(raw_data):
    """
    Main function to convert pkl data to Map object.
    
    Args:
        raw_data: dict containing 'map_polygon', 'map_point', and edge data
    
    Returns:
        Map object
    """
    map_polygon_data = raw_data['map_polygon']
    map_point_data = raw_data['map_point']
    map_point_to_polygon_data = raw_data[('map_point', 'to', 'map_polygon')]
    map_polygon_to_polygon_data = raw_data[('map_polygon', 'to', 'map_polygon')]
    
    map_obj = decode_map_features_from_tensor_data(
        map_polygon_data, 
        map_point_data, 
        map_point_to_polygon_data, 
        map_polygon_to_polygon_data
    )
    
    return map_obj
    
def calculate_traj_mask_uncentered(raw_data):
    # Get actual number of agents (could be less than 12)
    agent_data = raw_data['agent']
    num_agents = agent_data['num_nodes']
    
    # Initialize arrays with actual number of agents
    hist_trajs_uncentered = np.zeros((num_agents, history_timesteps, 6), dtype=np.float32)
    hist_valid = np.zeros((num_agents, history_timesteps), dtype=np.float32)
    fut_trajs_uncentered = np.zeros((num_agents, future_timesteps, 2), dtype=np.float32)
    fut_valid = np.zeros((num_agents, future_timesteps), dtype=np.float32)
    
    # Convert torch tensors to numpy arrays explicitly
    position = agent_data['position'].numpy() if hasattr(agent_data['position'], 'numpy') else agent_data['position']
    heading = agent_data['heading'].numpy() if hasattr(agent_data['heading'], 'numpy') else agent_data['heading']
    velocity = agent_data['velocity'].numpy() if hasattr(agent_data['velocity'], 'numpy') else agent_data['velocity']
    agent_type = agent_data['type'].numpy() if hasattr(agent_data['type'], 'numpy') else agent_data['type']
    valid_mask = agent_data['valid_mask'].numpy() if hasattr(agent_data['valid_mask'], 'numpy') else agent_data['valid_mask']
    predict_mask = agent_data['predict_mask'].numpy() if hasattr(agent_data['predict_mask'], 'numpy') else agent_data['predict_mask']
    
    # Fill in history trajectories (use actual number of agents)
    hist_trajs_uncentered[:, :, 0:2] = position[:num_agents, :history_timesteps, :2]  # x, y
    hist_trajs_uncentered[:, :, 2] = heading[:num_agents, :history_timesteps]  # heading
    hist_trajs_uncentered[:, :, 3:5] = velocity[:num_agents, :history_timesteps, :2]  # v_x, v_y
    hist_trajs_uncentered[:, :, 5] = agent_type[:num_agents, np.newaxis]  # type (broadcast across timesteps)
    
    # Fill in history valid mask
    hist_valid = valid_mask[:num_agents, :history_timesteps]
    
    # Fill in future trajectories
    fut_trajs_uncentered[:, :, 0:2] = position[:num_agents, history_timesteps:history_timesteps+future_timesteps, :2]
    
    # Fill in future valid mask
    fut_valid = predict_mask[:num_agents, history_timesteps:history_timesteps+future_timesteps]
    
    return hist_trajs_uncentered, hist_valid, fut_trajs_uncentered, fut_valid

if __name__ == '__main__':
    import logging
    import sys
    from datetime import datetime

    # === Logging setup ===
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_dir = "./logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"process_waymo_{timestamp}.log")

    # Configure logging to both file and console
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

    logging.info("=== Waymo data processing started ===")
    logging.info(f"PID: {os.getpid()}")
    logging.info(f"Logging to: {log_file}")

    # === Process data ===
    all_data = {
        training_prefix: (train_files, output_path_training),
        validation_prefix: (validation_files, output_path_validation),
        testing_prefix: (testing_files, output_path_testing)
    }

    for input_prefix, (input_files, output_path) in all_data.items():
        logging.info(f"Processing {len(input_files)} files from {input_prefix}")

        for i in tqdm(range(len(input_files))):
            try:
                raw_data = pd.read_pickle(input_files[i])
                scenario_id = raw_data['scenario_id']
                tqdm.write(f"Processing scenario {scenario_id}")
                logging.info(f"Processing scenario {scenario_id}")

                # Compute features
                hist_trajs_uncentered, hist_valid, fut_gt_trajs_uncentered, fut_valid = calculate_traj_mask_uncentered(raw_data)

                num_agents = hist_trajs_uncentered.shape[0]
                trajectory_data = {
                    j: {
                        'traj': hist_trajs_uncentered[j],
                        'valid': hist_valid[j],
                        'sub_class': object_type_class.get(int(raw_data['agent']['type'][j]), 'Other')
                    }
                    for j in range(num_agents)
                }
                future_gt_data = {
                    j: {'traj': fut_gt_trajs_uncentered[j], 'valid': fut_valid[j]}
                    for j in range(num_agents)
                }

                map_obj = build_map_polyline_from_pkl(raw_data)
                map_polyline = decode_map_features_from_proto(map_obj.map_features)

                agent_ids = raw_data['agent']['id']
                if hasattr(agent_ids, 'numpy'):
                    agent_ids = agent_ids.numpy()
                elif isinstance(agent_ids, list):
                    agent_ids = np.array(agent_ids)

                for ki in range(num_agents):
                    k = agent_ids[ki]
                    agent_trajectory_data = trajectory_data[ki]
                    
                    print(f"Agent {ki}: valid history = {np.sum(agent_trajectory_data['valid'][0:history_timesteps])}")
                    
                    # need there to be at least history_timesteps - 1 valid points = 11 - 1 = 10
                    # only consider agents with 10 valid history points
                    if np.sum(agent_trajectory_data['valid'][0:history_timesteps]) != history_timesteps - 1:
                        continue

                    inputs = process_model_input(trajectory_data, ki, map_polyline, future_gt_data)
                    output_file = os.path.join(output_path, f"{scenario_id}_{int(k)}.pkl")

                    with open(output_file, 'wb') as f:
                        pickle.dump(inputs, f)
                        print(f"Saving output to {output_file}")
                        
                    if agent_trajectory_data['sub_class'] in vehicle_class:
                        # make sure that agent is vehicle and duplicate data 5 times
                        for d in range(5):
                            inputs = process_model_input(trajectory_data, ki, map_polyline, future_gt_data)
                            output_file = os.path.join(output_path, f"{scenario_id}_{int(k)}_{d+1}.pkl")
                            with open(output_file, 'wb') as f:
                                print(f"Saving output (where subclass is vehicle) to {output_file}")
                                pickle.dump(inputs, f)

            except Exception as e:
                logging.exception(f"Error processing file {input_files[i]}: {e}")

    logging.info("=== Processing complete ===")
