# import yaml
# import random
# import pickle
# import glob
# import numpy as np
# import pandas as pd
# from torch.utils.data import Dataset
# from pathlib import Path


# """
# Loaded object type: <class 'dict'>
# Length (len()): 7
# Number of keys: 7
# First 20 keys (repr) and types:
# 0: type=str, repr='scenario_id'
# 1: type=str, repr='city'
# 2: type=str, repr='agent'
# 3: type=str, repr='map_polygon'
# 4: type=str, repr='map_point'
# 5: type=tuple, repr=('map_point', 'to', 'map_polygon')
# 6: type=tuple, repr=('map_polygon', 'to', 'map_polygon')
# """
# """
# Loaded type: <class 'dict'>
# key='scenario_id'                                                                                                             type=str                   len=16
# key='city'                                                                                                                    type=float64               len=None
# key='agent'                                                                                                                   type=dict                  len=11
# key='map_polygon'                                                                                                             type=dict                  len=3
# key='map_point'                                                                                                               type=dict                  len=6
# key=('map_point', 'to', 'map_polygon')                                                                                        type=dict                  len=1
# key=('map_polygon', 'to', 'map_polygon')                                                                                      type=dict                  len=2
# """
# # View a small sample of the trainig and validation to understand what I'm dealing with
# def load_data(data_path):
#     with open(data_path, 'rb') as file:
#         data = pickle.load(file) 
#     return data

# def get_item(entire_data):
#     # inputs = {'hist_trajs': hist_trajs, 'maps': maps, 
#     #             'hist_valid': hist_valid, 'fut_gt_trajs': fut_trajs, 
#     #             'fut_valid': fut_valid}
#     inputs = {'scenario_id': entire_data['scenario_id'],
#               'city': entire_data['city'],
#                 'agent': entire_data['agent'],
#                 'map_polygon': entire_data['map_polygon'],
#                 'map_point': entire_data['map_point'],
#                 'map_point_to_map_polygon': entire_data[('map_point', 'to', 'map_polygon')],
#                 'map_polygon_to_map_polygon': entire_data[('map_polygon', 'to', 'map_polygon')]}
#     return inputs

# def save_to_csvs(data, output_prefix):
#     # Save scenario-level data
#     scenario_data = pd.DataFrame([{
#         'scenario_id': data['scenario_id'],
#         'city': data['city']
#     }])
#     scenario_data.to_csv(f"{output_prefix}_scenario.csv", index=False)
    
#     # Save agent data (if it's a dict of arrays)
#     agent_dict = data['agent']
#     if isinstance(agent_dict, dict):
#         # Try to convert to DataFrame
#         agent_df = pd.DataFrame(agent_dict)
#         agent_df.to_csv(f"{output_prefix}_agents.csv", index=False)
    
#     # Save map polygon data
#     map_polygon_dict = data['map_polygon']
#     if isinstance(map_polygon_dict, dict):
#         map_polygon_df = pd.DataFrame(map_polygon_dict)
#         map_polygon_df.to_csv(f"{output_prefix}_map_polygons.csv", index=False)
    
#     # Save map point data
#     map_point_dict = data['map_point']
#     if isinstance(map_point_dict, dict):
#         map_point_df = pd.DataFrame(map_point_dict)
#         map_point_df.to_csv(f"{output_prefix}_map_points.csv", index=False)

# def main1():
#     training_path = "/data2/dataset/waymo/scenario_processed/training/1a0a6d4655106262.pkl"
#     training_data = load_data(training_path)
    
#     save_to_csvs(training_data, "/data/robert/CP-X-Prediction/MTR/training_sample.csv")

    
# def main2():
#     training_path = "/data2/dataset/waymo/scenario_processed/training/1a0a6d4655106262.pkl"
#     validaiton_path = "/data2/dataset/waymo/scenario_processed/validation/1a00ab7997996ea.pkl"
#     training_inputs = get_item(entire_data=load_data(training_path))
#     training_df = pd.DataFrame([training_inputs])
#     print(training_df.head())
#     validation_inputs = get_item(entire_data=load_data(validaiton_path))
#     validation_df = pd.DataFrame([validation_inputs])
#     print(validation_df.head())
    
#     training_df.to_csv("/data/robert/CP-X-Prediction/MTR/training_sample.csv", index=False)
#     validation_df.to_csv("/data/robert/CP-X-Prediction/MTR/validation_sample.csv", index=False)
    
# def main3():
#     training_path = "/data2/dataset/waymo/scenario_processed/training/1a0a6d4655106262.pkl"
#     training_data = load_data(training_path)
#     with open("/data/robert/CP-X-Prediction/MTR/training_sample.txt", "wb") as f:
#         f.write(repr(training_data).encode('utf-8'))
# if __name__ == "__main__":
#     # main1()

#     # pkl_path = Path("/data2/dataset/waymo/scenario_processed/training/1a0a6d4655106262.pkl")
#     # with pkl_path.open("rb") as f:
#     #     obj = pickle.load(f)

#     # print("Loaded type:", type(obj))
#     # if isinstance(obj, dict):
#     #     for k, v in obj.items():
#     #         try:
#     #             ln = len(v)
#     #         except Exception:
#     #             ln = None
#     #         print(f"key={repr(k)[:120]:120s}  type={type(v).__name__:20s}  len={ln}")
#     # else:
#     #     print("Top-level is not a dict; repr(obj)[:500]:", repr(obj)[:500])
#     main3()
import pickle
import torch
import numpy as np

def load_data(data_path):
    with open(data_path, 'rb') as file:
        data = pickle.load(file)
    return data

def print_tensor_info(name, tensor, indent=0):
    """Print detailed info about a tensor"""
    prefix = "  " * indent
    if isinstance(tensor, torch.Tensor):
        print(f"{prefix}{name}:")
        print(f"{prefix}  Shape: {tensor.shape}")
        print(f"{prefix}  Dtype: {tensor.dtype}")
        print(f"{prefix}  Device: {tensor.device}")
        print(f"{prefix}  Min: {tensor.min().item() if tensor.numel() > 0 else 'N/A'}")
        print(f"{prefix}  Max: {tensor.max().item() if tensor.numel() > 0 else 'N/A'}")
        print(f"{prefix}  Mean: {tensor.float().mean().item() if tensor.numel() > 0 else 'N/A'}")
        print(f"{prefix}  Non-zero elements: {torch.count_nonzero(tensor).item()}")
        print(f"{prefix}  First few values: {tensor.flatten()[:5].tolist()}")
    else:
        print(f"{prefix}{name}: {tensor}")

def print_dict_structure(data, indent=0, max_depth=5):
    """Recursively print dictionary structure"""
    if indent > max_depth:
        return
    
    prefix = "  " * indent
    
    if isinstance(data, dict):
        for key, value in data.items():
            print(f"\n{prefix}[{key}]:")
            
            if isinstance(value, dict):
                print(f"{prefix}  Type: dict with {len(value)} keys")
                print_dict_structure(value, indent + 1, max_depth)
            elif isinstance(value, torch.Tensor):
                print_tensor_info(key, value, indent + 1)
            elif isinstance(value, list):
                print(f"{prefix}  Type: list with {len(value)} elements")
                print(f"{prefix}  First few: {value[:5]}")
            else:
                print(f"{prefix}  Type: {type(value).__name__}")
                print(f"{prefix}  Value: {value}")
    elif isinstance(data, torch.Tensor):
        print_tensor_info("tensor", data, indent)
    else:
        print(f"{prefix}Value: {data}")

def analyze_masks(data):
    """Analyze valid_mask and predict_mask patterns"""
    print("\n" + "="*80)
    print("MASK ANALYSIS")
    print("="*80)
    
    agent_data = data['agent']
    num_agents = agent_data['num_nodes']
    
    valid_mask = agent_data['valid_mask']
    predict_mask = agent_data['predict_mask']
    
    print(f"\nNumber of agents: {num_agents}")
    print(f"AV index: {agent_data['av_index']}")
    print(f"\nAgent types: {agent_data['type'].tolist()}")
    print(f"Agent categories: {agent_data['category'].tolist()}")
    print(f"Agent IDs: {agent_data['id']}")
    
    print("\n" + "-"*80)
    print("Per-agent mask summary:")
    print("-"*80)
    
    for i in range(num_agents):
        agent_id = agent_data['id'][i]
        agent_type = agent_data['type'][i].item()
        agent_cat = agent_data['category'][i].item()
        
        valid_count = valid_mask[i].sum().item()
        predict_count = predict_mask[i].sum().item()
        
        # Find first and last valid timestep
        valid_indices = torch.where(valid_mask[i])[0]
        first_valid = valid_indices[0].item() if len(valid_indices) > 0 else -1
        last_valid = valid_indices[-1].item() if len(valid_indices) > 0 else -1
        
        # Find first and last predict timestep
        predict_indices = torch.where(predict_mask[i])[0]
        first_predict = predict_indices[0].item() if len(predict_indices) > 0 else -1
        last_predict = predict_indices[-1].item() if len(predict_indices) > 0 else -1
        
        is_av = " (AV)" if i == agent_data['av_index'] else ""
        
        print(f"\nAgent {i}{is_av} (ID: {agent_id}, Type: {agent_type}, Cat: {agent_cat}):")
        print(f"  Valid timesteps: {valid_count}/{valid_mask.shape[1]} (t={first_valid} to t={last_valid})")
        print(f"  Predict timesteps: {predict_count}/{predict_mask.shape[1]} (t={first_predict} to t={last_predict})")
        
        # Show first 20 and last 10 timesteps
        print(f"  Valid pattern (first 20): {valid_mask[i, :20].int().tolist()}")
        print(f"  Predict pattern (last 10): {predict_mask[i, -10:].int().tolist()}")

def analyze_trajectories(data):
    """Analyze trajectory data"""
    print("\n" + "="*80)
    print("TRAJECTORY ANALYSIS")
    print("="*80)
    
    agent_data = data['agent']
    positions = agent_data['position']
    velocities = agent_data['velocity']
    headings = agent_data['heading']
    
    num_agents, num_timesteps, _ = positions.shape
    
    print(f"\nPosition tensor shape: {positions.shape}")
    print(f"Velocity tensor shape: {velocities.shape}")
    print(f"Heading tensor shape: {headings.shape}")
    
    print("\n" + "-"*80)
    print("Per-agent trajectory summary:")
    print("-"*80)
    
    for i in range(num_agents):
        valid_mask = agent_data['valid_mask'][i]
        valid_positions = positions[i, valid_mask]
        
        if len(valid_positions) > 0:
            # Calculate travel distance
            diffs = valid_positions[1:, :2] - valid_positions[:-1, :2]
            distances = torch.norm(diffs, dim=1)
            total_distance = distances.sum().item()
            
            # Get velocity statistics
            valid_velocities = velocities[i, valid_mask]
            speeds = torch.norm(valid_velocities[:, :2], dim=1)
            
            print(f"\nAgent {i}:")
            print(f"  Start position: ({valid_positions[0, 0]:.2f}, {valid_positions[0, 1]:.2f})")
            print(f"  End position: ({valid_positions[-1, 0]:.2f}, {valid_positions[-1, 1]:.2f})")
            print(f"  Total distance traveled: {total_distance:.2f} m")
            print(f"  Average speed: {speeds.mean().item():.2f} m/s")
            print(f"  Max speed: {speeds.max().item():.2f} m/s")

def analyze_map(data):
    """Analyze map data"""
    print("\n" + "="*80)
    print("MAP ANALYSIS")
    print("="*80)
    
    map_polygon = data['map_polygon']
    map_point = data['map_point']
    point_to_polygon = data[('map_point', 'to', 'map_polygon')]
    polygon_to_polygon = data[('map_polygon', 'to', 'map_polygon')]
    
    print(f"\nMap polygons: {map_polygon['num_nodes']}")
    print(f"Map points: {map_point['num_nodes']}")
    
    # Analyze polygon types
    polygon_types = map_polygon['type']
    unique_types, counts = torch.unique(polygon_types, return_counts=True)
    print(f"\nPolygon type distribution:")
    for ptype, count in zip(unique_types, counts):
        print(f"  Type {ptype}: {count} polygons")
    
    # Analyze light types
    light_types = map_polygon['light_type']
    unique_lights, light_counts = torch.unique(light_types, return_counts=True)
    print(f"\nLight type distribution:")
    for ltype, count in zip(unique_lights, light_counts):
        print(f"  Light type {ltype}: {count} polygons")
    
    # Analyze point types
    point_types = map_point['type']
    unique_ptypes, ptype_counts = torch.unique(point_types, return_counts=True)
    print(f"\nPoint type distribution:")
    for ptype, count in zip(unique_ptypes, ptype_counts):
        print(f"  Type {ptype}: {count} points")
    
    # Analyze edges
    print(f"\nPoint-to-polygon edges: {point_to_polygon['edge_index'].shape[1]}")
    print(f"Polygon-to-polygon edges: {polygon_to_polygon['edge_index'].shape[1]}")
    
    # Analyze polygon-to-polygon edge types
    if 'type' in polygon_to_polygon:
        edge_types = polygon_to_polygon['type']
        unique_etypes, etype_counts = torch.unique(edge_types, return_counts=True)
        print(f"\nPolygon-to-polygon edge type distribution:")
        for etype, count in zip(unique_etypes, etype_counts):
            print(f"  Edge type {etype}: {count} edges")
    
    # Map bounds
    positions = map_point['position']
    print(f"\nMap bounds:")
    print(f"  X: [{positions[:, 0].min():.2f}, {positions[:, 0].max():.2f}]")
    print(f"  Y: [{positions[:, 1].min():.2f}, {positions[:, 1].max():.2f}]")
    print(f"  Z: [{positions[:, 2].min():.2f}, {positions[:, 2].max():.2f}]")

def main():
    training_path = "/data2/dataset/waymo/scenario_processed/training/1a0a6d4655106262.pkl"
    
    print("="*80)
    print("LOADING DATA")
    print("="*80)
    training_data = load_data(training_path)
    
    print(f"\nLoaded data type: {type(training_data)}")
    print(f"Top-level keys: {list(training_data.keys())}")
    
    # Print basic info
    print("\n" + "="*80)
    print("BASIC INFORMATION")
    print("="*80)
    print(f"Scenario ID: {training_data['scenario_id']}")
    print(f"City: {training_data['city']}")
    
    # Print full structure
    print("\n" + "="*80)
    print("FULL DATA STRUCTURE")
    print("="*80)
    print_dict_structure(training_data, max_depth=3)
    
    # Analyze masks
    analyze_masks(training_data)
    
    # Analyze trajectories
    analyze_trajectories(training_data)
    
    # Analyze map
    analyze_map(training_data)
    
    # Save full representation to file
    output_path = "/data/robert/CP-X-Prediction/MTR/training_sample_analysis.txt"
    with open(output_path, "w") as f:
        f.write("="*80 + "\n")
        f.write("FULL DATA REPRESENTATION\n")
        f.write("="*80 + "\n\n")
        f.write(repr(training_data))
    
    print(f"\n\nFull representation saved to: {output_path}")

if __name__ == "__main__":
    main()