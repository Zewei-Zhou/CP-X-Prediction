"""
Improved train_utils.py for Waymo Open Motion Dataset
Compatible with the improved MTR model

Key improvements:
1. Proper coordinate normalization
2. Better handling of edge cases
3. Compatible collate function
4. Data validation
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
    'TYPE_VEHICLE': 1,
    'TYPE_PEDESTRIAN': 2,
    'TYPE_CYCLIST': 3,
    'TYPE_OTHER': 4,
}


def load_config(file_path):
    """Load configuration from YAML file."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    
    # Handle nested config structure
    if 'config' in data:
        return data['config']
    return data


def collate_fn(batch):
    """
    Custom collate function to handle variable-sized maps.
    
    Args:
        batch: List of samples from WaymoDataset
        
    Returns:
        Batched tensors with padded maps
    """
    # Filter out None samples
    batch = [s for s in batch if s is not None]
    
    if len(batch) == 0:
        # Return minimal valid batch
        return {
            'hist_trajs': torch.zeros(1, 5, 11, 6),
            'hist_valid': torch.zeros(1, 5, 11),
            'fut_gt_trajs': torch.zeros(1, 5, 80, 2),
            'fut_valid': torch.zeros(1, 5, 80),
            'maps': torch.zeros(1, 1, 10, 4),
        }
    
    # Find max number of map polylines
    max_map_polylines = max(sample['maps'].shape[0] for sample in batch)
    batch_size = len(batch)
    
    # Get dimensions from first sample
    num_agents = batch[0]['hist_trajs'].shape[0]
    hist_steps = batch[0]['hist_trajs'].shape[1]
    fut_steps = batch[0]['fut_gt_trajs'].shape[1]
    points_per_polyline = batch[0]['maps'].shape[1]
    
    # Initialize tensors
    batch_dict = {
        'hist_trajs': torch.zeros(batch_size, num_agents, hist_steps, 6),
        'hist_valid': torch.zeros(batch_size, num_agents, hist_steps),
        'fut_gt_trajs': torch.zeros(batch_size, num_agents, fut_steps, 2),
        'fut_valid': torch.zeros(batch_size, num_agents, fut_steps),
        'maps': torch.zeros(batch_size, max_map_polylines, points_per_polyline, 4),
    }
    
    # Fill batch
    for i, sample in enumerate(batch):
        batch_dict['hist_trajs'][i] = torch.from_numpy(sample['hist_trajs']).float()
        batch_dict['hist_valid'][i] = torch.from_numpy(sample['hist_valid']).float()
        batch_dict['fut_gt_trajs'][i] = torch.from_numpy(sample['fut_gt_trajs']).float()
        batch_dict['fut_valid'][i] = torch.from_numpy(sample['fut_valid']).float()
        
        num_polylines = sample['maps'].shape[0]
        batch_dict['maps'][i, :num_polylines] = torch.from_numpy(sample['maps']).float()
    
    # Validate - replace any NaN/Inf
    for key, tensor in batch_dict.items():
        if not torch.isfinite(tensor).all():
            print(f"WARNING: NaN/Inf in collate batch['{key}'], replacing with zeros")
            batch_dict[key] = torch.where(torch.isfinite(tensor), tensor, torch.zeros_like(tensor))
    
    return batch_dict


class WaymoDataset(Dataset):
    """
    Dataset for Waymo Open Motion Dataset.
    
    Output format (compatible with improved MTR model):
        - hist_trajs: (N, 11, 6) [x, y, heading, vx, vy, type]
        - hist_valid: (N, 11) validity mask
        - fut_gt_trajs: (N, 80, 2) [x, y] future positions
        - fut_valid: (N, 80) validity mask
        - maps: (M, 10, 4) [x, y, direction, type]
    
    All coordinates are in agent-centric frame (center agent at origin).
    """
    
    def __init__(
        self, 
        data_path, 
        num_agents=5, 
        history_steps=11, 
        future_steps=80,
        points_per_polyline=10, 
        subset_fraction=1.0, 
        random_seed=42,
        max_map_range=150.0,  # Clip to ±150m (reasonable for 8s prediction)
        max_polylines=256,    # Limit polylines for memory
    ):
        self.data_list = []
        
        # Handle list or string input
        if isinstance(data_path, str):
            data_path = [data_path]
        
        for path in data_path:
            self.data_list.extend(glob.glob(f"{path}/*.pkl"))
        
        self.data_list.sort()
        total_files = len(self.data_list)
        
        # Subset selection
        if subset_fraction < 1.0:
            random.seed(random_seed)
            num_samples = int(total_files * subset_fraction)
            self.data_list = sorted(random.sample(self.data_list, num_samples))
            print(f"Using {num_samples}/{total_files} samples ({subset_fraction*100:.1f}%)")
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
        return len(self.data_list)
    
    def __getitem__(self, idx):
        try:
            return self._load_sample(idx)
        except Exception as e:
            print(f"WARNING: Failed to load sample {idx}: {e}")
            return self._empty_sample()
    
    def _empty_sample(self):
        """Return a valid empty sample."""
        return {
            'hist_trajs': np.zeros((self.num_agents, self.history_steps, 6), dtype=np.float32),
            'hist_valid': np.zeros((self.num_agents, self.history_steps), dtype=np.float32),
            'fut_gt_trajs': np.zeros((self.num_agents, self.future_steps, 2), dtype=np.float32),
            'fut_valid': np.zeros((self.num_agents, self.future_steps), dtype=np.float32),
            'maps': np.zeros((1, self.points_per_polyline, 4), dtype=np.float32),
        }
    
    def _transform_coords(self, x, y, cx, cy, cos_h, sin_h):
        """Transform to agent-centric coordinates."""
        dx, dy = x - cx, y - cy
        return dx * cos_h - dy * sin_h, dx * sin_h + dy * cos_h
    
    def _clip(self, x, y):
        """Clip coordinates to max_map_range."""
        return (
            np.clip(x, -self.max_map_range, self.max_map_range),
            np.clip(y, -self.max_map_range, self.max_map_range)
        )
    
    def _load_sample(self, idx):
        """Load and process a single sample."""
        with open(self.data_list[idx], 'rb') as f:
            data = pickle.load(f)
        
        current_time_idx = data['current_time_index']
        track_infos = data['track_infos']
        tracks_to_predict = data['tracks_to_predict']
        predict_indices = tracks_to_predict['track_index']
        
        if len(predict_indices) == 0:
            return self._empty_sample()
        
        # Select agents
        agent_indices = predict_indices[:min(len(predict_indices), self.num_agents)]
        
        # Get center agent state for coordinate transformation
        center_idx = agent_indices[0]
        center_traj = track_infos['trajs'][center_idx]
        center_state = center_traj[current_time_idx]
        
        cx, cy = center_state[0], center_state[1]
        center_heading = center_state[6]
        
        # Validate center state
        if not np.all(np.isfinite([cx, cy, center_heading])):
            return self._empty_sample()
        
        cos_h, sin_h = np.cos(-center_heading), np.sin(-center_heading)
        
        # Initialize outputs
        hist_trajs = np.zeros((self.num_agents, self.history_steps, 6), dtype=np.float32)
        hist_valid = np.zeros((self.num_agents, self.history_steps), dtype=np.float32)
        fut_gt_trajs = np.zeros((self.num_agents, self.future_steps, 2), dtype=np.float32)
        fut_valid = np.zeros((self.num_agents, self.future_steps), dtype=np.float32)
        
        # Process each agent
        for i, agent_idx in enumerate(agent_indices):
            traj = track_infos['trajs'][agent_idx]
            obj_type = track_infos['object_type'][agent_idx]
            type_id = TYPE_MAPPING.get(obj_type, 4)
            
            # === History ===
            hist_start = max(0, current_time_idx - self.history_steps + 1)
            hist_end = current_time_idx + 1
            hist_traj = traj[hist_start:hist_end]
            
            # Pad if needed
            if len(hist_traj) < self.history_steps:
                pad = np.zeros((self.history_steps - len(hist_traj), 10), dtype=np.float32)
                hist_traj = np.concatenate([pad, hist_traj], axis=0)
            
            for t in range(self.history_steps):
                if hist_traj[t, 9] > 0:  # valid flag
                    x, y = self._transform_coords(
                        hist_traj[t, 0], hist_traj[t, 1], cx, cy, cos_h, sin_h
                    )
                    x, y = self._clip(x, y)
                    
                    heading = hist_traj[t, 6] - center_heading
                    heading = np.arctan2(np.sin(heading), np.cos(heading))  # Normalize
                    
                    vx, vy = hist_traj[t, 7], hist_traj[t, 8]
                    vx_rot = vx * cos_h - vy * sin_h
                    vy_rot = vx * sin_h + vy * cos_h
                    vx_rot = np.clip(vx_rot, -50, 50)
                    vy_rot = np.clip(vy_rot, -50, 50)
                    
                    if np.all(np.isfinite([x, y, heading, vx_rot, vy_rot])):
                        hist_trajs[i, t] = [x, y, heading, vx_rot, vy_rot, type_id]
                        hist_valid[i, t] = 1.0
            
            # === Future ===
            fut_start = current_time_idx + 1
            fut_end = min(current_time_idx + self.future_steps + 1, len(traj))
            fut_traj = traj[fut_start:fut_end]
            
            for t in range(min(len(fut_traj), self.future_steps)):
                if fut_traj[t, 9] > 0:
                    x, y = self._transform_coords(
                        fut_traj[t, 0], fut_traj[t, 1], cx, cy, cos_h, sin_h
                    )
                    x, y = self._clip(x, y)
                    
                    if np.all(np.isfinite([x, y])):
                        fut_gt_trajs[i, t] = [x, y]
                        fut_valid[i, t] = 1.0
        
        # === Map Processing ===
        all_polylines = data['map_infos']['all_polylines']
        maps = []
        
        for i in range(0, len(all_polylines), self.points_per_polyline):
            segment = all_polylines[i:i + self.points_per_polyline]
            
            # Pad if needed
            if len(segment) < self.points_per_polyline:
                pad = np.zeros((self.points_per_polyline - len(segment), 7), dtype=np.float32)
                segment = np.concatenate([segment, pad], axis=0)
            
            polyline = np.zeros((self.points_per_polyline, 4), dtype=np.float32)
            
            for j in range(self.points_per_polyline):
                x, y = self._transform_coords(
                    segment[j, 0], segment[j, 1], cx, cy, cos_h, sin_h
                )
                x, y = self._clip(x, y)
                
                direction = np.arctan2(segment[j, 4], segment[j, 3]) - center_heading
                direction = np.arctan2(np.sin(direction), np.cos(direction))
                
                poly_type = int(segment[j, 6]) if np.isfinite(segment[j, 6]) else 0
                poly_type = max(0, min(7, poly_type))
                
                if np.all(np.isfinite([x, y, direction])):
                    polyline[j] = [x, y, direction, poly_type]
            
            maps.append(polyline)
        
        maps = np.array(maps, dtype=np.float32) if maps else np.zeros((1, self.points_per_polyline, 4), dtype=np.float32)
        
        # Limit polylines (keep closest)
        if len(maps) > self.max_polylines:
            distances = np.sqrt(maps[:, 0, 0]**2 + maps[:, 0, 1]**2 + 1e-6)
            closest = np.argsort(distances)[:self.max_polylines]
            maps = maps[closest]
        
        return {
            'hist_trajs': hist_trajs,
            'hist_valid': hist_valid,
            'fut_gt_trajs': fut_gt_trajs,
            'fut_valid': fut_valid,
            'maps': maps,
        }


def batch_nms(pred_trajs, pred_scores, dist_thresh=3, num_ret_modes=6):
    """
    Batch Non-Maximum Suppression for trajectory predictions.
    
    Args:
        pred_trajs: (B, K, T, 2) predicted trajectories
        pred_scores: (B, K) mode scores
        dist_thresh: distance threshold for suppression
        num_ret_modes: number of modes to return
        
    Returns:
        ret_trajs: (B, num_ret_modes, T, 2)
        ret_scores: (B, num_ret_modes)
        ret_idxs: (B, num_ret_modes)
    """
    B, K, T, D = pred_trajs.shape
    
    sorted_idxs = pred_scores.argsort(dim=-1, descending=True)
    bs_idx = torch.arange(B, device=pred_trajs.device)[:, None].expand(-1, K)
    
    sorted_scores = pred_scores[bs_idx, sorted_idxs]
    sorted_trajs = pred_trajs[bs_idx, sorted_idxs]
    sorted_goals = sorted_trajs[:, :, -1, :2]
    
    # Pairwise distances
    dist = (sorted_goals[:, :, None] - sorted_goals[:, None, :]).norm(dim=-1)
    cover_mask = dist < dist_thresh
    
    point_val = sorted_scores.clone()
    selected = torch.zeros_like(point_val)
    
    ret_idxs = torch.zeros(B, num_ret_modes, dtype=torch.long, device=pred_trajs.device)
    ret_trajs = torch.zeros(B, num_ret_modes, T, D, device=pred_trajs.device)
    ret_scores = torch.zeros(B, num_ret_modes, device=pred_trajs.device)
    
    for k in range(num_ret_modes):
        cur_idx = point_val.argmax(dim=-1)
        ret_idxs[:, k] = cur_idx
        ret_trajs[:, k] = sorted_trajs[bs_idx[:, 0], cur_idx]
        ret_scores[:, k] = sorted_scores[bs_idx[:, 0], cur_idx]
        
        # Suppress neighbors
        cover = cover_mask[bs_idx[:, 0], cur_idx]
        point_val = point_val * (~cover).float()
        selected[bs_idx[:, 0], cur_idx] = -1
        point_val = point_val + selected
    
    # Map back to original indices
    ret_idxs = sorted_idxs[bs_idx[:, :num_ret_modes], ret_idxs]
    
    return ret_trajs, ret_scores, ret_idxs


# Quick test
if __name__ == '__main__':
    import os
    from torch.utils.data import DataLoader
    
    test_path = "/data/dataset/CP-X/data/waymo/processed_scenarios_training"
    
    if os.path.exists(test_path):
        print("Testing WaymoDataset...")
        dataset = WaymoDataset(test_path, subset_fraction=0.01)
        print(f"Dataset size: {len(dataset)}")
        
        loader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=collate_fn)
        batch = next(iter(loader))
        
        print("\nBatch shapes:")
        for k, v in batch.items():
            print(f"  {k}: {v.shape}, range: [{v.min():.2f}, {v.max():.2f}]")
        
        print("\n✓ Dataset test passed!")