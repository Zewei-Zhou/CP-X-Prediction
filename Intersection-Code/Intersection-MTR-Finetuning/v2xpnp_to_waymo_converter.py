"""
v2xpnp_to_waymo_converter.py

Converts V2XPnP dataset to Waymo MTR format.
Window strategy: Non-overlapping when possible, minimal overlap when necessary.
Example: 150 frames → [0-90], [60-150] (only overlap to capture remaining data)
"""

import os
import yaml
import pickle
import numpy as np
from pathlib import Path
from tqdm import tqdm


# Object type mapping
OBJECT_TYPE_MAP = {
    'Car': 'TYPE_VEHICLE',
    'Van': 'TYPE_VEHICLE',
    'PoliceCar': 'TYPE_VEHICLE',
    'Bus': 'TYPE_VEHICLE',
    'LongVehicle': 'TYPE_VEHICLE',
    'Truck': 'TYPE_VEHICLE',
    'ConcreteTruck': 'TYPE_VEHICLE',
    'Pedestrian': 'TYPE_PEDESTRIAN',
    'Cyclist': 'TYPE_CYCLIST',
}

POLYLINE_TYPE = {'TYPE_SURFACE_STREET': 2}


def load_yaml_file(filepath):
    """Load YAML file."""
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)


def get_polyline_dir(polyline):
    """Calculate direction vectors for polyline."""
    polyline_pre = np.roll(polyline, shift=1, axis=0)
    polyline_pre[0] = polyline[0]
    diff = polyline - polyline_pre
    polyline_dir = diff / np.clip(np.linalg.norm(diff, axis=-1)[:, np.newaxis], 
                                   a_min=1e-6, a_max=1000000000)
    return polyline_dir


def calculate_window_positions(total_frames, window_size):
    """
    Calculate window positions with minimal overlap.
    
    Strategy:
    - Use non-overlapping windows when possible
    - Add one overlapping window at the end if needed
    
    Examples:
    - 150 frames, window=91 → [0-90], [60-150] (2 windows)
    - 91 frames, window=91 → [0-90] (1 window)
    - 180 frames, window=91 → [0-90], [91-181] (2 windows, no overlap)
    - 200 frames, window=91 → [0-90], [91-181], [110-200] (3 windows)
    """
    if total_frames < window_size:
        return []
    
    windows = []
    
    # Add non-overlapping windows
    pos = 0
    while pos + window_size <= total_frames:
        windows.append(pos)
        pos += window_size
    
    # If there are remaining frames, add one overlapping window
    remaining = total_frames - pos
    if remaining > 0:
        # Start the last window so it ends at total_frames
        last_window_start = total_frames - window_size
        windows.append(last_window_start)
    
    return windows


class V2XPnPToWaymoConverter:
    """Converter from V2XPnP to Waymo MTR format."""
    
    def __init__(self, config):
        self.config = config
        self.v2xpnp_root = Path(config['v2xpnp_root'])
        self.output_root = Path(config['output_root'])
        self.map_path = Path(config['map_path'])
        
        # Waymo format: 10 history + 1 current + 80 future = 91 total
        self.history_frames = 10
        self.future_frames = 80
        self.total_frames = 91
        self.fps = 10
        
        print("\n" + "="*80)
        print("V2XPnP to Waymo Converter")
        print("="*80)
        print(f"Input: {self.v2xpnp_root}")
        print(f"Output: {self.output_root}")
        print(f"Window size: {self.total_frames} frames")
        print(f"Strategy: Non-overlapping windows, minimal overlap when necessary")
        print("="*80)
        
        # Load maps
        print("\nLoading maps...")
        self.maps = self._load_maps()
    
    def convert_all_splits(self):
        """Convert all splits."""
        splits = ['train', 'val', 'test']
        
        for split_name in splits:
            print(f"\n{'='*80}")
            print(f"Converting {split_name.upper()} split")
            print(f"{'='*80}\n")
            
            self.convert_split(split_name)
    
    def convert_split(self, split_name):
        """Convert one split."""
        split_dir = self.v2xpnp_root / split_name
        if not split_dir.exists():
            print(f"⚠ Warning: {split_dir} does not exist, skipping")
            return
        
        # Determine output folder name
        if split_name == 'train':
            output_folder = 'processed_scenarios_training'
            info_suffix = 'training'
        else:
            output_folder = 'processed_scenarios_validation'
            info_suffix = 'val' if split_name == 'val' else 'validation'
        
        processed_dir = self.output_root / output_folder
        processed_dir.mkdir(parents=True, exist_ok=True)
        
        # Find scenarios
        scenarios = sorted([d for d in split_dir.iterdir() if d.is_dir()])
        print(f"Found {len(scenarios)} scenarios")
        
        # Process all scenarios
        info_list = []
        total_samples = 0
        
        for scenario_path in tqdm(scenarios, desc=f"Processing {split_name}"):
            scenario_infos, num_samples = self._process_scenario(scenario_path, processed_dir)
            info_list.extend(scenario_infos)
            total_samples += num_samples
        
        # Save info file
        info_filename = f'processed_scenarios_{info_suffix}_infos.pkl'
        info_path = self.output_root / info_filename
        
        with open(info_path, 'wb') as f:
            pickle.dump(info_list, f)
        
        print(f"\n{'='*60}")
        print(f"Results for {split_name.upper()}:")
        print(f"  Scenarios: {len(scenarios)}")
        print(f"  Samples: {total_samples}")
        print(f"  Avg samples/scenario: {total_samples / max(len(scenarios), 1):.1f}")
        print(f"  Output: {processed_dir}")
        print(f"  Info: {info_path}")
        print(f"{'='*60}")
    
    def _process_scenario(self, scenario_path, output_dir):
        """Process one scenario."""
        scenario_name = scenario_path.name
        
        # Load data
        scenario_data = self._load_scenario_data(scenario_path)
        
        if not scenario_data['timestamps']:
            return [], 0
        
        # Determine map
        map_type = self._determine_map_type(scenario_data['cav_ids'])
        map_infos = self.maps[map_type]
        
        timestamps = sorted(scenario_data['timestamps'])
        total_frames = len(timestamps)
        
        # Calculate window positions
        window_positions = calculate_window_positions(total_frames, self.total_frames)
        
        if not window_positions:
            return [], 0
        
        # Create samples
        info_list = []
        num_samples = 0
        
        for window_start in window_positions:
            current_idx = window_start + self.history_frames
            window_end = window_start + self.total_frames
            
            sample, info = self._create_sample_and_info(
                scenario_data,
                timestamps,
                window_start,
                current_idx,
                window_end,
                map_infos,
                scenario_name
            )
            
            if sample and info:
                scenario_id = sample['scenario_id']
                sample_file = output_dir / f'sample_{scenario_id}.pkl'
                
                with open(sample_file, 'wb') as f:
                    pickle.dump(sample, f)
                
                info_list.append(info)
                num_samples += 1
        
        return info_list, num_samples
    
    def _load_scenario_data(self, scenario_path):
        """Load all data from a scenario."""
        cav_folders = sorted([d for d in scenario_path.iterdir() if d.is_dir()])
        cav_ids = [cav.name for cav in cav_folders]
        
        # Determine ego (first positive CAV ID)
        ego_cav_id = cav_ids[0]
        for cav_id in cav_ids:
            try:
                if int(cav_id) > 0:
                    ego_cav_id = cav_id
                    break
            except:
                pass
        
        # Collect timestamps and agents
        timestamps = set()
        agents = {}
        
        for cav_folder in cav_folders:
            cav_id = cav_folder.name
            
            yaml_files = sorted([
                f for f in cav_folder.glob('*.yaml')
                if 'additional' not in f.name and 'camera_gt' not in f.name
            ])
            
            for yaml_file in yaml_files:
                timestamp = yaml_file.stem
                timestamps.add(timestamp)
                
                data = load_yaml_file(yaml_file)
                
                if 'vehicles' in data:
                    for agent_id, agent_data in data['vehicles'].items():
                        key = (timestamp, agent_id)
                        
                        loc = agent_data['location']
                        ctr = agent_data['center']
                        
                        agents[key] = {
                            'id': agent_id,
                            'position': [
                                loc[0] + ctr[0],
                                loc[1] + ctr[1],
                                loc[2] + ctr[2]
                            ],
                            'heading': np.radians(agent_data['angle'][1]),
                            'size': agent_data['extent'],
                            'type': agent_data['obj_type'],
                            'cav_id': cav_id
                        }
        
        return {
            'cav_ids': cav_ids,
            'timestamps': timestamps,
            'agents': agents,
            'ego_cav_id': ego_cav_id
        }
    
    def _create_sample_and_info(self, scenario_data, timestamps, window_start, 
                                current_idx, window_end, map_infos, scenario_name):
        """Create one sample and info entry."""
        # Get agent IDs in window
        window_timestamps = timestamps[window_start:window_end]
        agent_ids = set()
        
        for ts in window_timestamps:
            for (t, aid) in scenario_data['agents'].keys():
                if t == ts:
                    agent_ids.add(aid)
        
        agent_ids = sorted(agent_ids)
        
        if len(agent_ids) == 0:
            return None, None
        
        # Build trajectories: (num_agents, 91, 10)
        trajs = np.zeros((len(agent_ids), self.total_frames, 10), dtype=np.float32)
        object_types = []
        
        for agent_idx, agent_id in enumerate(agent_ids):
            prev_pos = None
            agent_type = None
            
            for t_idx in range(self.total_frames):
                ts_idx = window_start + t_idx
                
                if ts_idx >= len(timestamps):
                    break
                
                ts = timestamps[ts_idx]
                key = (ts, agent_id)
                
                if key in scenario_data['agents']:
                    adata = scenario_data['agents'][key]
                    
                    trajs[agent_idx, t_idx, 0:3] = adata['position']
                    trajs[agent_idx, t_idx, 3:6] = adata['size']
                    trajs[agent_idx, t_idx, 6] = adata['heading']
                    
                    if prev_pos is not None:
                        dt = 1.0 / self.fps
                        vx = (adata['position'][0] - prev_pos[0]) / dt
                        vy = (adata['position'][1] - prev_pos[1]) / dt
                        trajs[agent_idx, t_idx, 7] = vx
                        trajs[agent_idx, t_idx, 8] = vy
                    
                    trajs[agent_idx, t_idx, 9] = 1.0
                    
                    prev_pos = adata['position']
                    
                    if agent_type is None:
                        agent_type = OBJECT_TYPE_MAP.get(adata['type'], 'TYPE_VEHICLE')
            
            object_types.append(agent_type or 'TYPE_VEHICLE')
        
        # Find SDC
        ego_cav_id = scenario_data['ego_cav_id']
        sdc_track_index = 0
        
        for i, aid in enumerate(agent_ids):
            for (ts, agent_id), adata in scenario_data['agents'].items():
                if agent_id == aid and adata['cav_id'] == ego_cav_id:
                    sdc_track_index = i
                    break
        
        # Tracks to predict
        tracks_to_predict_indices = []
        tracks_to_predict_types = []
        tracks_to_predict_difficulty = []
        
        for i in range(len(agent_ids)):
            if trajs[i, self.history_frames, 9] > 0:
                if trajs[i, self.history_frames + 1:, 9].sum() > 0:
                    tracks_to_predict_indices.append(i)
                    tracks_to_predict_types.append(object_types[i])
                    tracks_to_predict_difficulty.append(0)
        
        # Timestamps
        timestamps_seconds = [t * 0.1 for t in range(self.total_frames)]
        
        # Scenario ID
        scenario_id = f"{scenario_name}_{timestamps[window_start]}"
        
        # Sample
        sample = {
            'scenario_id': scenario_id,
            'timestamps_seconds': timestamps_seconds,
            'current_time_index': self.history_frames,
            'sdc_track_index': sdc_track_index,
            'objects_of_interest': [],
            'tracks_to_predict': {
                'track_index': tracks_to_predict_indices,
                'difficulty': tracks_to_predict_difficulty,
                'object_type': tracks_to_predict_types
            },
            'track_infos': {
                'object_id': agent_ids,
                'object_type': object_types,
                'trajs': trajs
            },
            'map_infos': map_infos,
            'dynamic_map_infos': {
                'lane_id': [],
                'state': [],
                'stop_point': []
            }
        }
        
        # Info
        info = {
            'scenario_id': scenario_id,
            'timestamps_seconds': timestamps_seconds,
            'current_time_index': self.history_frames,
            'sdc_track_index': sdc_track_index,
            'objects_of_interest': [],
            'tracks_to_predict': {
                'track_index': tracks_to_predict_indices,
                'difficulty': tracks_to_predict_difficulty,
                'object_type': tracks_to_predict_types
            }
        }
        
        return sample, info
    
    def _determine_map_type(self, cav_ids):
        """Determine map type."""
        for cav_id in cav_ids:
            try:
                if int(cav_id) < 0:
                    return 'intersection'
            except:
                pass
        return 'corridor'
    
    def _load_maps(self):
        """Load maps."""
        maps = {}
        
        intersection_file = self.map_path / 'v2x_intersection_vector_map.pkl'
        if intersection_file.exists():
            with open(intersection_file, 'rb') as f:
                vector_map = pickle.load(f)
            maps['intersection'] = self._convert_map_features(vector_map.map_features)
            print(f"  ✓ Intersection map: {maps['intersection']['all_polylines'].shape[0]} points")
        
        corridor_file = self.map_path / 'v2v_corridors_vector_map.pkl'
        if corridor_file.exists():
            with open(corridor_file, 'rb') as f:
                vector_map = pickle.load(f)
            maps['corridor'] = self._convert_map_features(vector_map.map_features)
            print(f"  ✓ Corridor map: {maps['corridor']['all_polylines'].shape[0]} points")
        
        return maps
    
    def _convert_map_features(self, map_features):
        """Convert map features."""
        polylines = []
        
        for feature in map_features:
            if hasattr(feature, 'polyline') and hasattr(feature, 'type'):
                points = np.array([[p.x, p.y, p.z] for p in feature.polyline], dtype=np.float32)
                
                if len(points) == 0:
                    continue
                
                dirs = get_polyline_dir(points)
                global_type = POLYLINE_TYPE.get('TYPE_SURFACE_STREET', 2)
                types = np.full((len(points), 1), global_type, dtype=np.float32)
                
                polyline = np.concatenate([points, dirs, types], axis=1)
                polylines.append(polyline)
        
        if len(polylines) > 0:
            all_polylines = np.concatenate(polylines, axis=0).astype(np.float32)
        else:
            all_polylines = np.zeros((0, 7), dtype=np.float32)
        
        return {
            'all_polylines': all_polylines,
            'lane': [],
            'road_line': [],
            'road_edge': [],
            'stop_sign': [],
            'crosswalk': [],
            'speed_bump': []
        }


def main():
    """Main entry point."""
    
    config = {
        'v2xpnp_root': '/data/dataset/v2x-real-pnp',
        'output_root': '/data/dataset/waymo_finetune_v2xpnp',
        'map_path': '/data/dataset/v2x-real-pnp/map',
    }
    
    converter = V2XPnPToWaymoConverter(config)
    converter.convert_all_splits()
    
    print("\n" + "="*80)
    print("✓ Conversion Complete!")
    print(f"✓ Output: {config['output_root']}")
    print("\nOutput structure:")
    print("  train/ → processed_scenarios_training/")
    print("        → processed_scenarios_training_infos.pkl")
    print("  val/   → processed_scenarios_validation/")
    print("        → processed_scenarios_val_infos.pkl")
    print("  test/  → processed_scenarios_validation/")
    print("        → processed_scenarios_validation_infos.pkl")
    print("="*80 + "\n")


if __name__ == '__main__':
    main()
    

# ## What This Does

# **Window Strategy:**
# - 150 frames → `[0-90]`, `[60-150]` (2 windows, minimal overlap)
# - 91 frames → `[0-90]` (1 window)
# - 180 frames → `[0-90]`, `[91-180]` (2 windows, no overlap)

# **Output:**
# /data/dataset/waymo_finetune_v2xpnp/
# ├── processed_scenarios_training/
# ├── processed_scenarios_training_infos.pkl
# ├── processed_scenarios_validation/
# └── processed_scenarios_val_infos.pkl

## The Code Flow

# Input Structure:
# /data/dataset/v2x-real-pnp/
# ├── train/
# │   ├── 2023-03-17-15-53-02_1_0/          ← Scenario folder
# │   │   ├── -2/                           ← CAV folder (infrastructure)
# │   │   │   ├── 000000.yaml              ← Frame files
# │   │   │   ├── 000001.yaml
# │   │   │   └── ...
# │   │   ├── -1/                           ← CAV folder (infrastructure)
# │   │   ├── 1/                            ← CAV folder (vehicle)
# │   │   └── 2/                            ← CAV folder (vehicle)
# │   └── 2023-03-17-16-10-45_2_1/
# └── map/
#     ├── v2x_intersection_vector_map.pkl
#     └── v2v_corridors_vector_map.pkl

# ↓ [Code processes this] ↓

# Output Structure:
# /data/dataset/waymo_finetune_v2xpnp/
# ├── processed_scenarios_training/
# │   ├── sample_2023-03-17-15-53-02_1_0_000000.pkl
# │   ├── sample_2023-03-17-15-53-02_1_0_000060.pkl
# │   └── ...
# └── processed_scenarios_training_infos.pkl
