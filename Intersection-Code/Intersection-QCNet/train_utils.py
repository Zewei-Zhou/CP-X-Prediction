"""
Enhanced train_utils.py with RAW Waymo data processing on-the-fly
Includes support for using a subset of the training data for pretraining

Features:
- Processes raw Waymo files during training (no preprocessing needed)
- Can limit dataset to a fraction (e.g., 1/2 or 1/3) for pretraining
- Maintains all original functionality
"""

import yaml
import torch
import pickle
import glob
import numpy as np
from torch.utils.data import Dataset
import random


# Type mapping for Waymo object types
TYPE_MAPPING = {
    'TYPE_UNSET': 0,
    'TYPE_VEHICLE': 0,
    'TYPE_PEDESTRIAN': 1,
    'TYPE_CYCLIST': 2,
    'TYPE_OTHER': 3,
}


def load_config(file_path):
    """Load configuration from YAML file."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def collate_fn(batch):
    """
    Custom collate function to handle variable-sized maps.
    Pads maps to the maximum size in the batch.
    
    Args:
        batch: List of samples from WaymoDataset
        
    Returns:
        Batched tensors with padded maps
    """
    # Find max number of map polylines in this batch
    max_map_polylines = max([sample['maps'].shape[0] for sample in batch])
    
    batch_size = len(batch)
    
    # Initialize batch tensors
    batch_dict = {
        'hist_trajs': torch.zeros(batch_size, 5, 11, 6),
        'hist_valid': torch.zeros(batch_size, 5, 11),
        'fut_gt_trajs': torch.zeros(batch_size, 5, 80, 2),
        'fut_valid': torch.zeros(batch_size, 5, 80),
        'maps': torch.zeros(batch_size, max_map_polylines, 10, 4),
    }
    
    # Fill in the batch
    for i, sample in enumerate(batch):
        batch_dict['hist_trajs'][i] = torch.from_numpy(sample['hist_trajs'])
        batch_dict['hist_valid'][i] = torch.from_numpy(sample['hist_valid'])
        batch_dict['fut_gt_trajs'][i] = torch.from_numpy(sample['fut_gt_trajs'])
        batch_dict['fut_valid'][i] = torch.from_numpy(sample['fut_valid'])
        
        # Pad maps to max_map_polylines
        num_polylines = sample['maps'].shape[0]
        batch_dict['maps'][i, :num_polylines] = torch.from_numpy(sample['maps'])
        # Remaining polylines stay as zeros (padding)
    
    return batch_dict


class WaymoDataset(Dataset):
    """
    Dataset for loading RAW Waymo Open Motion Dataset samples.
    Processes raw Waymo scenario files on-the-fly.
    
    NEW FEATURE: Support for using a subset of data for pretraining!
    
    Output sample contains:
        - hist_trajs: (5, 11, 6) [x, y, heading, vx, vy, type]
        - hist_valid: (5, 11) validity mask for history
        - fut_gt_trajs: (5, 80, 2) [x, y] future trajectories
        - fut_valid: (5, 80) validity mask for future
        - maps: (M, 10, 4) [x, y, dir, type] map polylines (M varies by sample)
    """
    
    def __init__(self, data_path, num_agents=5, history_steps=11, future_steps=80, 
                 points_per_polyline=10, subset_fraction=1.0, random_seed=42,
                 max_map_range=None, max_polylines=512):
        """
        Args:
            data_path (list or str): Path(s) to directory with RAW .pkl files
            num_agents (int): Number of agents per sample (default: 5)
            history_steps (int): Number of history timesteps (default: 11)
            future_steps (int): Number of future timesteps (default: 80)
            points_per_polyline (int): Points per map polyline (default: 10)
            subset_fraction (float): Fraction of dataset to use (0.0-1.0, default: 1.0)
                                    Set to 0.5 for 1/2, 0.33 for 1/3, etc.
            random_seed (int): Seed for reproducible subset selection
            max_map_range (float): If set, clip map coordinates to this range in meters
                                  (e.g., 200 for ±200m around agent). None = no clipping.
            max_polylines (int): Maximum number of map polylines per sample (default: 512)
                                Limits memory usage. Typical scenes have 500-3000 polylines.
        """
        self.data_list = []
        
        # Handle both list and string inputs
        if isinstance(data_path, str):
            data_path = [data_path]
        
        # Collect all .pkl files from specified paths
        for path in data_path:
            pkl_files = glob.glob(path + '/*.pkl')
            self.data_list.extend(pkl_files)
        
        # Sort for reproducibility
        self.data_list.sort()
        
        total_files = len(self.data_list)
        
        # Apply subset fraction if specified
        if subset_fraction < 1.0:
            # Set random seed for reproducibility
            random.seed(random_seed)
            
            # Calculate number of samples to use
            num_samples = int(total_files * subset_fraction)
            
            # Randomly sample the subset
            self.data_list = random.sample(self.data_list, num_samples)
            
            # Sort again for consistent ordering
            self.data_list.sort()
            
            print(f"Using {num_samples}/{total_files} samples ({subset_fraction*100:.1f}% of dataset)")
        else:
            print(f"Using full dataset: {total_files} samples")
        
        if len(self.data_list) == 0:
            raise ValueError(f"No .pkl files found in {data_path}")
        
        self.num_agents = num_agents
        self.history_steps = history_steps
        self.future_steps = future_steps
        self.points_per_polyline = points_per_polyline
        self.max_map_range = max_map_range
        self.max_polylines = max_polylines
    
    def __len__(self):
        """Return total number of samples."""
        return len(self.data_list)
    
    def _transform_coordinates(self, x, y, center_x, center_y, cos_h, sin_h):
        """Transform to center agent's coordinate frame"""
        dx = x - center_x
        dy = y - center_y
        x_rot = dx * cos_h - dy * sin_h
        y_rot = dx * sin_h + dy * cos_h
        return x_rot, y_rot
    
    def __getitem__(self, idx):
        """
        Get a single sample, processing raw Waymo data on-the-fly.
        
        Args:
            idx (int): Sample index
            
        Returns:
            dict: Sample with keys matching model expectations
        """
        # Load raw data from file
        with open(self.data_list[idx], 'rb') as file:
            data = pickle.load(file)
        
        # Get basic info
        current_time_idx = data['current_time_index']
        track_infos = data['track_infos']
        tracks_to_predict = data['tracks_to_predict']
        
        # Get agents to predict
        predict_indices = tracks_to_predict['track_index']
        
        # Handle edge case: no agents to predict
        if len(predict_indices) == 0:
            # Return zero-filled sample
            return {
                'hist_trajs': np.zeros((self.num_agents, self.history_steps, 6), dtype=np.float32),
                'hist_valid': np.zeros((self.num_agents, self.history_steps), dtype=np.float32),
                'fut_gt_trajs': np.zeros((self.num_agents, self.future_steps, 2), dtype=np.float32),
                'fut_valid': np.zeros((self.num_agents, self.future_steps), dtype=np.float32),
                'maps': np.zeros((1, self.points_per_polyline, 4), dtype=np.float32),
            }
        
        # Limit to num_agents
        num_valid_agents = min(len(predict_indices), self.num_agents)
        agent_indices = predict_indices[:num_valid_agents]
        
        # Initialize arrays
        hist_trajs = np.zeros((self.num_agents, self.history_steps, 6), dtype=np.float32)
        hist_valid = np.zeros((self.num_agents, self.history_steps), dtype=np.float32)
        fut_gt_trajs = np.zeros((self.num_agents, self.future_steps, 2), dtype=np.float32)
        fut_valid = np.zeros((self.num_agents, self.future_steps), dtype=np.float32)
        
        # Get center agent (first agent to predict)
        center_idx = agent_indices[0]
        center_traj = track_infos['trajs'][center_idx]
        center_state = center_traj[current_time_idx]
        
        center_x, center_y = center_state[0], center_state[1]
        center_heading = center_state[6]
        
        # Validate center agent state - if invalid, return empty sample
        if not (np.isfinite(center_x) and np.isfinite(center_y) and np.isfinite(center_heading)):
            return {
                'hist_trajs': np.zeros((self.num_agents, self.history_steps, 6), dtype=np.float32),
                'hist_valid': np.zeros((self.num_agents, self.history_steps), dtype=np.float32),
                'fut_gt_trajs': np.zeros((self.num_agents, self.future_steps, 2), dtype=np.float32),
                'fut_valid': np.zeros((self.num_agents, self.future_steps), dtype=np.float32),
                'maps': np.zeros((1, self.points_per_polyline, 4), dtype=np.float32),
            }
        
        # Rotation matrix
        cos_h = np.cos(-center_heading)
        sin_h = np.sin(-center_heading)
        
        # Process each agent
        for i, agent_idx in enumerate(agent_indices):
            traj = track_infos['trajs'][agent_idx]
            obj_type = track_infos['object_type'][agent_idx]
            type_id = TYPE_MAPPING.get(obj_type, 3)
            
            # Extract history
            hist_start = max(0, current_time_idx - self.history_steps + 1)
            hist_end = current_time_idx + 1
            hist_traj = traj[hist_start:hist_end]
            
            # Pad if needed
            if len(hist_traj) < self.history_steps:
                padding = np.zeros((self.history_steps - len(hist_traj), 10), dtype=np.float32)
                hist_traj = np.concatenate([padding, hist_traj], axis=0)
            
            # Extract features: [x, y, heading, vx, vy, type]
            for t in range(self.history_steps):
                if hist_traj[t, 9] > 0:  # valid flag
                    x, y = self._transform_coordinates(
                        hist_traj[t, 0], hist_traj[t, 1],
                        center_x, center_y, cos_h, sin_h
                    )
                    heading = hist_traj[t, 6] - center_heading
                    vx, vy = hist_traj[t, 7], hist_traj[t, 8]
                    
                    # Rotate velocity
                    vx_rot = vx * cos_h - vy * sin_h
                    vy_rot = vx * sin_h + vy * cos_h
                    
                    # Check for NaN/inf values and skip if invalid
                    if np.isfinite(x) and np.isfinite(y) and np.isfinite(heading) and \
                       np.isfinite(vx_rot) and np.isfinite(vy_rot):
                        hist_trajs[i, t] = [x, y, heading, vx_rot, vy_rot, type_id]
                        hist_valid[i, t] = 1.0
            
            # Extract future
            fut_start = current_time_idx + 1
            fut_end = min(current_time_idx + self.future_steps + 1, len(traj))
            fut_traj = traj[fut_start:fut_end]
            
            for t in range(len(fut_traj)):
                if t < self.future_steps and fut_traj[t, 9] > 0:
                    x, y = self._transform_coordinates(
                        fut_traj[t, 0], fut_traj[t, 1],
                        center_x, center_y, cos_h, sin_h
                    )
                    # Check for NaN/inf values
                    if np.isfinite(x) and np.isfinite(y):
                        fut_gt_trajs[i, t] = [x, y]
                        fut_valid[i, t] = 1.0
        
        # Process map polylines
        all_polylines = data['map_infos']['all_polylines']
        
        # Reshape into fixed-size segments
        maps = []
        for i in range(0, len(all_polylines), self.points_per_polyline):
            polyline_points = all_polylines[i:i+self.points_per_polyline]
            
            if len(polyline_points) < self.points_per_polyline:
                padding = np.zeros((self.points_per_polyline - len(polyline_points), 7), 
                                 dtype=np.float32)
                polyline_points = np.concatenate([polyline_points, padding], axis=0)
            
            # Extract features: [x, y, dir, type]
            polyline_processed = np.zeros((self.points_per_polyline, 4), dtype=np.float32)
            for j in range(self.points_per_polyline):
                if j < len(polyline_points):
                    x, y = self._transform_coordinates(
                        polyline_points[j, 0], polyline_points[j, 1],
                        center_x, center_y, cos_h, sin_h
                    )
                    dir_x, dir_y = polyline_points[j, 3], polyline_points[j, 4]
                    direction = np.arctan2(dir_y, dir_x) - center_heading
                    poly_type = int(polyline_points[j, 6])
                    
                    # Check for NaN/inf values and set to zero if invalid
                    if not (np.isfinite(x) and np.isfinite(y) and np.isfinite(direction)):
                        x, y, direction = 0.0, 0.0, 0.0
                    
                    # Optionally clip map range to prevent very large values
                    if self.max_map_range is not None:
                        x = np.clip(x, -self.max_map_range, self.max_map_range)
                        y = np.clip(y, -self.max_map_range, self.max_map_range)
                    
                    # Ensure poly_type is valid (0-4)
                    poly_type = max(0, min(4, poly_type))
                    
                    polyline_processed[j] = [x, y, direction, poly_type]
            
            maps.append(polyline_processed)
        
        maps = np.array(maps, dtype=np.float32)
        
        # Handle empty maps
        if len(maps) == 0:
            maps = np.zeros((1, self.points_per_polyline, 4), dtype=np.float32)
        
        # Limit number of polylines to prevent OOM
        # Prioritize nearby polylines (smaller x,y values = closer to agent)
        if len(maps) > self.max_polylines:
            # Calculate distance of each polyline (use first point)
            distances = np.sqrt(maps[:, 0, 0]**2 + maps[:, 0, 1]**2 + 1e-7)
            # Get indices of closest polylines
            closest_indices = np.argsort(distances)[:self.max_polylines]
            maps = maps[closest_indices]
        
        return {
            'hist_trajs': hist_trajs,
            'hist_valid': hist_valid,
            'fut_gt_trajs': fut_gt_trajs,
            'fut_valid': fut_valid,
            'maps': maps
        }


def batch_nms(pred_trajs, pred_scores, dist_thresh=3, num_ret_modes=6):
    """
    Batch Non-Maximum Suppression for trajectory predictions.
    
    Args:
        pred_trajs (tensor): (batch_size, num_modes, num_timestamps, 2)
        pred_scores (tensor): (batch_size, num_modes)
        dist_thresh (float): Distance threshold for suppression
        num_ret_modes (int): Number of modes to return
        
    Returns:
        ret_trajs (tensor): (batch_size, num_ret_modes, num_timestamps, 2)
        ret_scores (tensor): (batch_size, num_ret_modes)
        ret_idxs (tensor): (batch_size, num_ret_modes)
    """
    batch_size, num_modes, num_timestamps, num_feat_dim = pred_trajs.shape

    sorted_idxs = pred_scores.argsort(dim=-1, descending=True)
    bs_idxs_full = torch.arange(batch_size).type_as(sorted_idxs)[:, None].repeat(1, num_modes)
    sorted_pred_scores = pred_scores[bs_idxs_full, sorted_idxs]
    sorted_pred_trajs = pred_trajs[bs_idxs_full, sorted_idxs]
    sorted_pred_goals = sorted_pred_trajs[:, :, -1, :]

    dist = (sorted_pred_goals[:, :, None, 0:2] - sorted_pred_goals[:, None, :, 0:2]).norm(dim=-1)
    point_cover_mask = (dist < dist_thresh)

    point_val = sorted_pred_scores.clone()
    point_val_selected = torch.zeros_like(point_val)

    ret_idxs = sorted_idxs.new_zeros(batch_size, num_ret_modes).long()
    ret_trajs = sorted_pred_trajs.new_zeros(batch_size, num_ret_modes, num_timestamps, num_feat_dim)
    ret_scores = sorted_pred_trajs.new_zeros(batch_size, num_ret_modes)
    bs_idxs = torch.arange(batch_size).type_as(ret_idxs)

    for k in range(num_ret_modes):
        cur_idx = point_val.argmax(dim=-1)
        ret_idxs[:, k] = cur_idx

        new_cover_mask = point_cover_mask[bs_idxs, cur_idx]
        point_val = point_val * (~new_cover_mask).float()
        point_val_selected[bs_idxs, cur_idx] = -1
        point_val += point_val_selected

        ret_trajs[:, k] = sorted_pred_trajs[bs_idxs, cur_idx]
        ret_scores[:, k] = sorted_pred_scores[bs_idxs, cur_idx]

    bs_idxs = torch.arange(batch_size).type_as(sorted_idxs)[:, None].repeat(1, num_ret_modes)
    ret_idxs = sorted_idxs[bs_idxs, ret_idxs]

    return ret_trajs, ret_scores, ret_idxs


# Test the dataset
if __name__ == '__main__':
    import os
    from torch.utils.data import DataLoader
    
    # Example usage with subset
    test_path = "/data/dataset/CP-X/data/waymo/processed_scenarios_training"
    
    if os.path.exists(test_path):
        print("Testing WaymoDataset with subset...")
        
        # Create dataset with 1/3 of data
        dataset = WaymoDataset(test_path, subset_fraction=0.33)
        print(f"Dataset: {len(dataset)} samples")
        
        # Create DataLoader with custom collate function
        dataloader = DataLoader(
            dataset,
            batch_size=4,
            shuffle=True,
            num_workers=0,
            collate_fn=collate_fn
        )
        
        # Load a batch
        print("\nLoading batch...")
        batch = next(iter(dataloader))
        
        print(f"Batch keys: {batch.keys()}")
        for key, value in batch.items():
            print(f"  {key}: {value.shape}")
        
        print("\n✓ WaymoDataset working correctly with subset!")
    else:
        print(f"Test path {test_path} does not exist")