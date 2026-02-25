"""
CORRECTED train_utils.py for Waymo Open Motion Dataset
Compatible with the improved MTR model

Fixes applied:
1. [CRITICAL] Map polyline splitting now respects segment boundaries
2. [CRITICAL] Agent type mapping handles both int and string types
3. [CRITICAL] Map type clipping expanded and properly bounded
4. [SERIOUS]  Aux loss no longer diluted by invalid frames (handled in model)
5. [SERIOUS]  Added data validation and debug utilities
6. [MODERATE] Improved edge case handling throughout
"""

import yaml
import torch
import pickle
import glob
import numpy as np
from torch.utils.data import Dataset
import random


# === Type mapping for Waymo object types ===
# Handles BOTH string keys (raw Waymo) and integer IDs (some preprocessors)
TYPE_MAPPING_STR = {
    'TYPE_UNSET': 0,
    'TYPE_VEHICLE': 1,
    'TYPE_PEDESTRIAN': 2,
    'TYPE_CYCLIST': 3,
    'TYPE_OTHER': 4,
}

# Integer type IDs (used by some Waymo preprocessors like MTR's)
TYPE_MAPPING_INT = {0: 0, 1: 1, 2: 2, 3: 3}  # Direct mapping for 0-3
# Anything else → 4 (OTHER)

# Waymo map polyline type mapping
# Raw Waymo types can range from 0 to 20+
# We map them down to a manageable range for embedding
POLYLINE_TYPE_MAPPING = {
    0: 0,   # UNDEFINED → padding
    1: 1,   # FREEWAY
    2: 1,   # SURFACE_STREET (group with freeway as "lane")
    3: 2,   # BIKE_LANE
    6: 3,   # TYPE_ROAD_LINE → road boundary
    7: 3,   # TYPE_ROAD_EDGE → road boundary
    8: 4,   # STOP_SIGN → traffic control
    9: 5,   # CROSSWALK
    10: 6,  # SPEED_BUMP
    11: 7,  # TYPE_DRIVEWAY
    12: 3,  # TYPE_ROAD_EDGE_CURB
    13: 3,  # TYPE_ROAD_EDGE_OTHER
    15: 4,  # TYPE_SIGNAL
    16: 4,  # TYPE_STOP_SIGN
    17: 5,  # TYPE_CROSSWALK
    18: 6,  # TYPE_SPEED_BUMP
}
MAX_POLYLINE_TYPE = 8  # Total types for embedding (padding 0 + 7 types)


def get_type_id(obj_type):
    """Convert Waymo object type to integer ID, handling both formats."""
    if isinstance(obj_type, str):
        return TYPE_MAPPING_STR.get(obj_type, 4)
    elif isinstance(obj_type, (int, np.integer, float, np.floating)):
        obj_type_int = int(obj_type)
        if 0 <= obj_type_int <= 3:
            return obj_type_int
        return 4  # OTHER for anything outside 0-3
    return 4


def get_polyline_type_id(raw_type):
    """Map raw Waymo polyline type to embedding index."""
    if not np.isfinite(raw_type):
        return 0
    raw_int = int(raw_type)
    return POLYLINE_TYPE_MAPPING.get(raw_int, min(raw_int, MAX_POLYLINE_TYPE - 1))


def load_config(file_path):
    """Load configuration from YAML file."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    if 'config' in data:
        return data['config']
    return data


def collate_fn(batch):
    """
    Custom collate function to handle variable-sized maps.
    Filters None samples and pads maps to max polyline count.
    """
    batch = [s for s in batch if s is not None]

    if len(batch) == 0:
        return {
            'hist_trajs': torch.zeros(1, 5, 11, 6),
            'hist_valid': torch.zeros(1, 5, 11),
            'fut_gt_trajs': torch.zeros(1, 5, 80, 2),
            'fut_valid': torch.zeros(1, 5, 80),
            'maps': torch.zeros(1, 1, 10, 4),
        }

    max_map_polylines = max(sample['maps'].shape[0] for sample in batch)
    batch_size = len(batch)

    num_agents = batch[0]['hist_trajs'].shape[0]
    hist_steps = batch[0]['hist_trajs'].shape[1]
    fut_steps = batch[0]['fut_gt_trajs'].shape[1]
    points_per_polyline = batch[0]['maps'].shape[1]

    batch_dict = {
        'hist_trajs': torch.zeros(batch_size, num_agents, hist_steps, 6),
        'hist_valid': torch.zeros(batch_size, num_agents, hist_steps),
        'fut_gt_trajs': torch.zeros(batch_size, num_agents, fut_steps, 2),
        'fut_valid': torch.zeros(batch_size, num_agents, fut_steps),
        'maps': torch.zeros(batch_size, max_map_polylines, points_per_polyline, 4),
    }

    for i, sample in enumerate(batch):
        batch_dict['hist_trajs'][i] = torch.from_numpy(sample['hist_trajs']).float()
        batch_dict['hist_valid'][i] = torch.from_numpy(sample['hist_valid']).float()
        batch_dict['fut_gt_trajs'][i] = torch.from_numpy(sample['fut_gt_trajs']).float()
        batch_dict['fut_valid'][i] = torch.from_numpy(sample['fut_valid']).float()

        num_polylines = sample['maps'].shape[0]
        batch_dict['maps'][i, :num_polylines] = torch.from_numpy(sample['maps']).float()

    # Validate — replace NaN/Inf
    for key, tensor in batch_dict.items():
        if not torch.isfinite(tensor).all():
            print(f"WARNING: NaN/Inf in collate batch['{key}'], replacing with zeros")
            batch_dict[key] = torch.where(torch.isfinite(tensor), tensor, torch.zeros_like(tensor))

    return batch_dict


class WaymoDataset(Dataset):
    """
    Dataset for Waymo Open Motion Dataset.

    Output format (compatible with MTR model):
        - hist_trajs: (N, 11, 6) [x, y, heading, vx, vy, type]
        - hist_valid: (N, 11) validity mask
        - fut_gt_trajs: (N, 80, 2) [x, y] future positions
        - fut_valid: (N, 80) validity mask
        - maps: (M, points_per_polyline, 4) [x, y, direction, type]

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
        max_map_range=150.0,
        max_polylines=256,
    ):
        self.data_list = []

        if isinstance(data_path, str):
            data_path = [data_path]

        for path in data_path:
            self.data_list.extend(glob.glob(f"{path}/*.pkl"))

        self.data_list.sort()
        total_files = len(self.data_list)

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
            print(f"WARNING: Failed to load sample {idx} ({self.data_list[idx]}): {e}")
            return self._empty_sample()

    def _empty_sample(self):
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
            np.clip(y, -self.max_map_range, self.max_map_range),
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

            # FIX BUG 3: Handle both string and integer type IDs
            type_id = get_type_id(obj_type)

            # === History ===
            hist_start = max(0, current_time_idx - self.history_steps + 1)
            hist_end = current_time_idx + 1
            hist_traj = traj[hist_start:hist_end]

            if len(hist_traj) < self.history_steps:
                pad = np.zeros((self.history_steps - len(hist_traj), traj.shape[1]), dtype=np.float32)
                hist_traj = np.concatenate([pad, hist_traj], axis=0)

            for t in range(self.history_steps):
                if hist_traj[t, 9] > 0:  # valid flag
                    x, y = self._transform_coords(
                        hist_traj[t, 0], hist_traj[t, 1], cx, cy, cos_h, sin_h
                    )
                    x, y = self._clip(x, y)

                    heading = hist_traj[t, 6] - center_heading
                    heading = np.arctan2(np.sin(heading), np.cos(heading))

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

        # === Map Processing — FIX BUG 1: Respect polyline boundaries ===
        maps = self._process_map(data, cx, cy, cos_h, sin_h, center_heading)

        # Sanity checks
        assert hist_trajs.shape == (self.num_agents, self.history_steps, 6), \
            f"hist_trajs shape mismatch: {hist_trajs.shape}"
        assert maps.shape[1] == self.points_per_polyline, \
            f"maps points_per_polyline mismatch: {maps.shape}"

        return {
            'hist_trajs': hist_trajs,
            'hist_valid': hist_valid,
            'fut_gt_trajs': fut_gt_trajs,
            'fut_valid': fut_valid,
            'maps': maps,
        }

    def _process_map(self, data, cx, cy, cos_h, sin_h, center_heading):
        """
        Process map polylines respecting segment boundaries.

        FIX: The original code split all_polylines into fixed chunks of
        points_per_polyline, crossing polyline boundaries. This fix detects
        boundaries by checking for discontinuities in position or type changes.
        """
        map_infos = data.get('map_infos', {})
        all_polylines = map_infos.get('all_polylines', None)

        if all_polylines is None or len(all_polylines) == 0:
            return np.zeros((1, self.points_per_polyline, 4), dtype=np.float32)

        # --- Detect polyline boundaries ---
        # A new polyline starts when:
        #   (a) the type (column 6) changes, OR
        #   (b) there's a large spatial gap between consecutive points
        SPATIAL_GAP_THRESHOLD = 3.0  # meters — points >3m apart likely different polylines

        types = all_polylines[:, 6] if all_polylines.shape[1] > 6 else np.zeros(len(all_polylines))

        # Compute spatial gaps
        positions = all_polylines[:, :2]
        gaps = np.linalg.norm(np.diff(positions, axis=0), axis=1)

        # Detect boundaries (type change OR large gap)
        type_changes = np.diff(types) != 0
        spatial_breaks = gaps > SPATIAL_GAP_THRESHOLD

        # Boundary indices (where a new polyline starts)
        boundaries = np.where(type_changes | spatial_breaks)[0] + 1
        boundaries = np.concatenate([[0], boundaries, [len(all_polylines)]])

        # --- Process each detected polyline ---
        maps = []
        for seg_idx in range(len(boundaries) - 1):
            start = boundaries[seg_idx]
            end = boundaries[seg_idx + 1]
            segment_points = all_polylines[start:end]

            if len(segment_points) == 0:
                continue

            # If segment is too long, split into sub-segments of points_per_polyline
            for sub_start in range(0, len(segment_points), self.points_per_polyline):
                sub_segment = segment_points[sub_start:sub_start + self.points_per_polyline]

                # Pad if needed
                if len(sub_segment) < self.points_per_polyline:
                    # Repeat last point for padding (better than zeros)
                    pad_count = self.points_per_polyline - len(sub_segment)
                    pad = np.tile(sub_segment[-1:], (pad_count, 1))
                    sub_segment = np.concatenate([sub_segment, pad], axis=0)

                polyline = np.zeros((self.points_per_polyline, 4), dtype=np.float32)

                for j in range(self.points_per_polyline):
                    x, y = self._transform_coords(
                        sub_segment[j, 0], sub_segment[j, 1], cx, cy, cos_h, sin_h
                    )
                    x, y = self._clip(x, y)

                    # Direction from dx/dy columns if available
                    if sub_segment.shape[1] > 4:
                        direction = np.arctan2(sub_segment[j, 4], sub_segment[j, 3]) - center_heading
                        direction = np.arctan2(np.sin(direction), np.cos(direction))
                    else:
                        direction = 0.0

                    # FIX BUG 2: Proper type mapping
                    raw_type = sub_segment[j, 6] if sub_segment.shape[1] > 6 else 0
                    poly_type = get_polyline_type_id(raw_type)

                    if np.all(np.isfinite([x, y, direction])):
                        polyline[j] = [x, y, direction, poly_type]

                maps.append(polyline)

        if len(maps) == 0:
            return np.zeros((1, self.points_per_polyline, 4), dtype=np.float32)

        maps = np.array(maps, dtype=np.float32)

        # Limit polylines — keep closest to center agent
        if len(maps) > self.max_polylines:
            # Distance from center of each polyline to origin
            center_points = maps[:, maps.shape[1] // 2, :2]  # Use middle point
            distances = np.sqrt(center_points[:, 0]**2 + center_points[:, 1]**2 + 1e-6)
            closest = np.argsort(distances)[:self.max_polylines]
            maps = maps[closest]

        return maps


# ============================================================
# Debug / Sanity Check Utilities
# ============================================================

def debug_print_sample(sample, label=""):
    """Print shapes and value ranges for a single sample."""
    print(f"\n{'='*60}")
    print(f"DEBUG SAMPLE {label}")
    print(f"{'='*60}")
    for key, val in sample.items():
        arr = val if isinstance(val, np.ndarray) else val.numpy()
        print(f"  {key:20s}: shape={str(arr.shape):20s} "
              f"range=[{arr.min():.3f}, {arr.max():.3f}]  "
              f"finite={np.all(np.isfinite(arr))}")

    # Specific checks
    ht = sample['hist_trajs']
    hv = sample['hist_valid']
    ft = sample['fut_gt_trajs']
    fv = sample['fut_valid']

    if isinstance(ht, torch.Tensor):
        ht, hv, ft, fv = ht.numpy(), hv.numpy(), ft.numpy(), fv.numpy()

    # Center agent at last timestep should be near origin
    center_last = ht[0, -1]
    print(f"\n  Center agent, last timestep: {center_last}")
    print(f"    → x,y should be near (0,0): ({center_last[0]:.4f}, {center_last[1]:.4f})")
    print(f"    → heading should be near 0: {center_last[2]:.4f}")

    # Check validity counts
    print(f"\n  History valid: {hv.sum():.0f}/{hv.size} "
          f"({100*hv.sum()/hv.size:.1f}%)")
    print(f"  Future valid:  {fv.sum():.0f}/{fv.size} "
          f"({100*fv.sum()/fv.size:.1f}%)")

    # Check center agent future trajectory
    center_fut = ft[0]  # (80, 2)
    center_fv = fv[0]   # (80,)
    valid_fut = center_fut[center_fv > 0]
    if len(valid_fut) > 0:
        displacements = np.linalg.norm(np.diff(valid_fut, axis=0), axis=1)
        print(f"\n  Center agent future: {len(valid_fut)} valid steps")
        print(f"    First 5 positions: {valid_fut[:5].tolist()}")
        print(f"    Mean step displacement: {displacements.mean():.3f} m")
        print(f"    Total displacement: {np.linalg.norm(valid_fut[-1] - valid_fut[0]):.3f} m")
    else:
        print(f"\n  ⚠️ Center agent has NO valid future timesteps!")

    # Check map polyline types
    maps = sample['maps'] if isinstance(sample['maps'], np.ndarray) else sample['maps'].numpy()
    types = maps[:, 0, -1]
    unique_types = np.unique(types[types > 0])
    print(f"\n  Map: {maps.shape[0]} polylines, types present: {unique_types}")
    max_type = types.max()
    if max_type > MAX_POLYLINE_TYPE:
        print(f"  ⚠️ MAX MAP TYPE {max_type} exceeds embedding size {MAX_POLYLINE_TYPE}!")


def verify_data_format_compatibility(waymo_sample, challenge_sample=None):
    """Verify Waymo dataset output matches what the model expects."""
    print("\n" + "="*60)
    print("FORMAT COMPATIBILITY CHECK")
    print("="*60)

    expected = {
        'hist_trajs': ('N', 11, 6),   # [x, y, heading, vx, vy, type]
        'hist_valid': ('N', 11),
        'fut_gt_trajs': ('N', 80, 2), # [x, y]
        'fut_valid': ('N', 80),
        'maps': ('M', 10, 4),         # [x, y, direction, type]
    }

    for key, expected_shape in expected.items():
        actual = waymo_sample[key].shape
        match = len(actual) == len(expected_shape)
        for i, (a, e) in enumerate(zip(actual, expected_shape)):
            if isinstance(e, int) and a != e:
                match = False
        status = "✓" if match else "✗"
        print(f"  {status} {key:20s}: expected {expected_shape}, got {actual}")

    # Type range checks
    ht = waymo_sample['hist_trajs']
    if isinstance(ht, torch.Tensor):
        ht = ht.numpy()
    types = ht[:, :, -1]  # Agent types
    valid_mask = waymo_sample['hist_valid']
    if isinstance(valid_mask, torch.Tensor):
        valid_mask = valid_mask.numpy()
    valid_types = types[valid_mask > 0]
    max_agent_type = valid_types.max() if len(valid_types) > 0 else 0
    print(f"\n  Agent types present: {np.unique(valid_types).astype(int)}")
    if max_agent_type > 21:
        print(f"  ⚠️ Agent type {max_agent_type} exceeds AgentEncoder embedding(22)!")
    else:
        print(f"  ✓ Agent types within embedding range")


# ============================================================
# Batch NMS (unchanged)
# ============================================================

def batch_nms(pred_trajs, pred_scores, dist_thresh=3, num_ret_modes=6):
    """Batch Non-Maximum Suppression for trajectory predictions."""
    B, K, T, D = pred_trajs.shape

    sorted_idxs = pred_scores.argsort(dim=-1, descending=True)
    bs_idx = torch.arange(B, device=pred_trajs.device)[:, None].expand(-1, K)

    sorted_scores = pred_scores[bs_idx, sorted_idxs]
    sorted_trajs = pred_trajs[bs_idx, sorted_idxs]
    sorted_goals = sorted_trajs[:, :, -1, :2]

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

        cover = cover_mask[bs_idx[:, 0], cur_idx]
        point_val = point_val * (~cover).float()
        selected[bs_idx[:, 0], cur_idx] = -1
        point_val = point_val + selected

    ret_idxs = sorted_idxs[bs_idx[:, :num_ret_modes], ret_idxs]

    return ret_trajs, ret_scores, ret_idxs


# ============================================================
# Quick self-test
# ============================================================
if __name__ == '__main__':
    import os
    from torch.utils.data import DataLoader

    test_path = "/data/dataset/CP-X/data/waymo/processed_scenarios_training"

    if os.path.exists(test_path):
        print("Testing WaymoDataset (CORRECTED)...")
        dataset = WaymoDataset(test_path, subset_fraction=0.001)
        print(f"Dataset size: {len(dataset)}")

        # Test single sample
        sample = dataset[0]
        debug_print_sample(sample, label="Sample 0")
        verify_data_format_compatibility(sample)

        # Test batch
        loader = DataLoader(dataset, batch_size=4, shuffle=True, collate_fn=collate_fn)
        batch = next(iter(loader))
        print("\nBatch shapes:")
        for k, v in batch.items():
            print(f"  {k}: {v.shape}, range: [{v.min():.2f}, {v.max():.2f}]")

        print("\n✓ Dataset test passed!")
    else:
        print(f"Test path not found: {test_path}")
        print("Skipping self-test. Run manually with your data path.")