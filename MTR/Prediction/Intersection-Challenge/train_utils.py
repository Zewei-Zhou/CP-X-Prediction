# Written by Robert Spataru

# Some code used and taken from the following source:
# Motion Transformer (MTR): https://arxiv.org/abs/2209.13508
# Published at NeurIPS 2022
# Written by Shaoshuai Shi 
# All Rights Reserved

import yaml
import torch
import random
import pickle
import glob
import pathlib
import numpy as np
from torch.utils.data import Dataset
import torch.nn.functional as F
from common_utils import create_logger
import common_utils
# from torch.nn.utils.rnn import pad_sequence
# from MTR_Paper.datasets.waymo.waymo_dataset import waymo_types
from maps import (
    MapPoint,
    LaneType,
    Lane,
    Crosswalk,
    RoadLine,
    WalkButton,
    Map,
)
def load_config(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    return data

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

    
class WaymoDataset(Dataset):
    
      # get infos
    """
    [{'scenario_id': 'b85e1bd6cc8e74c0', 'timestamps_seconds': 
    [0.0, 0.09998, 0.60018, 6.80025, 6.90027, 8.60011, 8.7001, 8.80005, 8.90003, 9.00002], 
    'current_time_index': 10, 'sdc_track_index': 13, 'objects_of_interest': [], 
    'tracks_to_predict': {'track_index': [0, 2], 'difficulty': [1, 1], 
    'object_type': ['TYPE_VEHICLE', 'TYPE_VEHICLE']}},
    """
    # PADDING = 0
    # LANE = 1
    # ROAD_LINE = 2
    # CROSSWALK = 3
    # OTHER = 4
    map_internal_encoding = {"Padding":0, "Lane":1, "RoadLine":2, "Crosswalk":3, "Other":4}
  
    
    def __init__(self, cfg, data_type, percent_data):
        self.dataset_cfg = cfg
        self.percent_data_used = percent_data
        self.mode = data_type
        self.data_root = cfg['DATA_ROOT']
        self.data_path = pathlib.Path(self.data_root) / cfg['SPLIT_DIR'][data_type]
        self.infos_path = pathlib.Path(self.data_root) / cfg['INFO_FILE'][data_type]
        self.log_file = cfg['log_file']
        self.logger = common_utils.create_logger(log_file=self.log_file)
        self.logger.info('**********************Start logging**********************')
        self.infos = self.get_all_infos(self.infos_path)
        self.logger.info(f'Total scenes after filters: {len(self.infos)}')
        # self.data_list = []
        # for path in data_path:
        #     self.data_list += glob.glob(path + '/*.pkl')

        self.history_timesteps = 11
        
    def get_all_infos(self, info_path):
        self.logger.info(f'Start to load infos from {info_path}')
        with open(info_path, 'rb') as f:
            src_infos = pickle.load(f)

        infos = src_infos[::self.dataset_cfg['SAMPLE_INTERVAL'][self.mode]]
        self.logger.info(f'Total scenes before filters: {len(infos)}')

        for func_name, val in self.dataset_cfg['INFO_FILTER_DICT'].items():
            infos = getattr(self, func_name)(infos, val)

         # If a fractional subset is requested (e.g. 0.5 for half) and we're in train mode,
        # pick a fixed deterministic subset so it does not change across epochs / runs.
        try:
            pct = float(self.percent_data_used)
        except Exception:
            pct = 1.0

        if self.mode == 'train' and 0.0 < pct < 1.0:
            total = len(infos)
            k = max(1, int(total * pct))
            seed = 42
            rng = random.Random(seed)
            selected_idx = sorted(rng.sample(range(total), k=k))
            infos = [infos[i] for i in selected_idx]
            self.logger.info(f'Selected deterministic subset: {k}/{total} scenes (pct={pct}, seed={seed})')

        return infos
    
    def filter_info_by_object_type(self, infos, valid_object_types=None):
        ret_infos = []
        for cur_info in infos:
            num_interested_agents = cur_info['tracks_to_predict']['track_index'].__len__()
            if num_interested_agents == 0:
                continue

            valid_mask = []
            for idx, cur_track_index in enumerate(cur_info['tracks_to_predict']['track_index']):
                valid_mask.append(cur_info['tracks_to_predict']['object_type'][idx] in valid_object_types)

            valid_mask = np.array(valid_mask) > 0
            if valid_mask.sum() == 0:
                continue

            assert len(cur_info['tracks_to_predict'].keys()) == 3, f"{cur_info['tracks_to_predict'].keys()}"
            cur_info['tracks_to_predict']['track_index'] = list(np.array(cur_info['tracks_to_predict']['track_index'])[valid_mask])
            cur_info['tracks_to_predict']['object_type'] = list(np.array(cur_info['tracks_to_predict']['object_type'])[valid_mask])
            cur_info['tracks_to_predict']['difficulty'] = list(np.array(cur_info['tracks_to_predict']['difficulty'])[valid_mask])

            ret_infos.append(cur_info)
        # self.logger.info(f'Total scenes after filter_info_by_object_type: {len(ret_infos)}')
        return ret_infos

    
    # def load_data(self, data_path):
    #     with open(data_path, 'rb') as file:
    #         data = pickle.load(file)
            
    #     return data
    
    # def __len__(self):
    #     return len(self.data_list)
    
    def map_object_to_simple_model_input(self, map_obj: Map, max_polylines=256) -> torch.Tensor:
        """
        Convert Map dataclass to model input format.
        
        Args:
            map_obj: Your Map dataclass with Lane, RoadLine, etc.
            
        Returns:
            maps_tensor: (M, W, 5) where M=num_polylines, W=20 points
        """
        
        """
        maps: [B, M, W, 5]
       ↓  ↓  ↓  ↓
       │  │  │  └─ 5 features per point
       │  │  └──── W = 20 points per polyline
       │  └─────── M = number of polylines (e.g., 256)
       └────────── B = batch size
        """
        # Index 0: Padding
        # Index 1: Lane (your Lane dataclass)
        # Index 2: RoadLine (your RoadLine dataclass)
        # Index 3: Crosswalk (your Crosswalk dataclass)
        # Index 4: Other (WalkButton, or any future features like RoadEdge, StopSign)
        # (0=pad, 1=lane, 2=line, 3=cross, 4=other)
        # only use the polyline part of the objects that make up Map objects
        # maps_tensor: (B, M, 20, 5)
        polylines = []
        for map_feature in map_obj.map_features:
            if isinstance(map_feature, Lane):
                polyline = map_feature.polyline
                polyline_type = 1
                
            elif isinstance(map_feature, RoadLine):
                polyline = map_feature.polyline
                polyline_type = 2
                    
            elif isinstance(map_feature, Crosswalk):
                polyline = map_feature.polygon
                polyline_type = 3
                
            elif isinstance(map_feature, WalkButton):
                polyline = map_feature.polygon
                polyline_type = 4
            else:
                # unknown type
                polyline = [MapPoint(x=0, y=0) for i in range(20)]
                polyline_type = 0

            polyline_array = np.zeros((20, 5), dtype=np.float32)
            for i, point in enumerate(polyline[:20]):
                polyline_array[i, 0] = point.x
                polyline_array[i, 1] = point.y
                polyline_array[i, 2] = 0.0  # z (optional)
                polyline_array[i, 3] = 0.0  # unused
                polyline_array[i, 4] = polyline_type
            
                
            polylines.append(polyline_array)

        polylines = polylines[:max_polylines]
        
        # if len(polylines) < max_polylines:
        #     # pad the polylines to reach max polylines
        #     polylines.append(np.zeros(max_polylines - len(polylines, 20, 5)), dtype=np.float32)
        # Pad if needed
        while len(polylines) < max_polylines:
            polylines.append(np.zeros((20, 5), dtype=np.float32))
           
        return torch.from_numpy(np.stack(polylines))
    
    def convert_dictionary_format(self, mtr_ret_dict):
        num_centers = mtr_ret_dict['obj_trajs'].shape[0]
        all_samples = []
        
        maps_tensor = mtr_ret_dict['maps'] 
        
        for center in range(num_centers):
            sample = self.convert_single_center(mtr_ret_dict=mtr_ret_dict, center_idx=center)
            # We don't need to add maps to 'sample' here anymore, we handle it below
            all_samples.append(sample)

        # 1. Stack the agents (Shape: [num_centers, 11, 6])
        hist_trajs = torch.stack([sample['hist_trajs'] for sample in all_samples])
        hist_valid = torch.stack([sample['hist_valid'] for sample in all_samples])
        fut_trajs = torch.stack([sample['fut_gt_trajs'] for sample in all_samples])
        fut_valid = torch.stack([sample['fut_valid'] for sample in all_samples])

        # 2. Stack the maps (Shape: [num_centers, 256, 20, 5])
        # We repeat the map 'num_centers' times so it matches hist_trajs
        maps_stacked = maps_tensor.unsqueeze(0).repeat(num_centers, 1, 1, 1)

        return {
            'maps': maps_stacked,         # <--- NOW THIS MATCHES hist_trajs
            'hist_trajs': hist_trajs,     
            'hist_valid': hist_valid,     
            'fut_gt_trajs': fut_trajs,   
            'fut_valid': fut_valid        
        }
        
    def convert_single_center(self, mtr_ret_dict, center_idx=0, max_agents=5):
        # only 3 centers
        obj_trajs = mtr_ret_dict['obj_trajs'][center_idx]  # (num_agents, 11, 29)
        obj_trajs_mask = mtr_ret_dict['obj_trajs_mask'][center_idx] # (num_agents, 11)
        current_num_agents = obj_trajs.shape[0]
        num_agents = min(current_num_agents, max_agents)
        
        # AGENT HISTORY
        # (num_agents=5, num_timesteps=11, num_features=6)
        # x, y, heading, v_x, v_y, type
        hist_trajs = np.zeros((max_agents, self.history_timesteps, 6), dtype=np.float32)
        hist_trajs[:num_agents, :, 0] = obj_trajs[:num_agents, :, 0] # x
        hist_trajs[:num_agents, :, 1] = obj_trajs[:num_agents, :, 1] # y
        hist_trajs[:num_agents, :, 2] = np.arctan2(                        # heading (from sin/cos)
            obj_trajs[:num_agents, :, 23],  # sin
            obj_trajs[:num_agents, :, 24]   # cos
        )
        hist_trajs[:num_agents, :, 3] = obj_trajs[:num_agents, :, 25]     # vx
        hist_trajs[:num_agents, :, 4] = obj_trajs[:num_agents, :, 26]     # vy
        # broadcast the type across all 11 timesteps since the type never changes
        hist_trajs[:num_agents, :, 5] = self.convert_type(mtr_ret_dict['obj_types'][:num_agents])[:, np.newaxis]  # type
        
        hist_valid = np.zeros((max_agents, self.history_timesteps), dtype=bool)
        hist_valid[:num_agents, :] = obj_trajs_mask[:num_agents, :]
        
        # AGENT FUTURE 
        # [x, y, vx, vy]
        obj_trajs_future_state = mtr_ret_dict['obj_trajs_future_state'][center_idx]  # (num_agents, 80, 4)
        obj_trajs_future_mask = mtr_ret_dict['obj_trajs_future_mask'][center_idx]
        
        # 80 future timesteps
        fut_gt_trajs = np.zeros((max_agents, 80, 2), dtype=np.float32)  # Only 2 features (x, y), not 6
        fut_gt_trajs[:num_agents, :, :] = obj_trajs_future_state[:num_agents, :, :2]
        
        fut_valid = np.zeros((max_agents, 80), dtype=bool)  # Should be 80 timesteps, not self.history_timesteps
        fut_valid[:num_agents, :] = obj_trajs_future_mask[:num_agents, :]
        
        # MAP
        maps = mtr_ret_dict['maps']
        return {
            'hist_trajs': torch.from_numpy(hist_trajs),
            'hist_valid': torch.from_numpy(hist_valid),
            'maps': maps,
            'fut_gt_trajs': torch.from_numpy(fut_gt_trajs),
            'fut_valid': torch.from_numpy(fut_valid)
        }

    def convert_type(self, obj_types):
        """Convert Waymo type strings to integers."""
        type_map = {
            'TYPE_UNSET': 0,
            'TYPE_VEHICLE': 1,
            'TYPE_PEDESTRIAN': 2,
            'TYPE_CYCLIST': 3,
            'TYPE_OTHER': 4,
        }
        return np.array([type_map.get(t, 0) for t in obj_types], dtype=np.int64)

    def __len__(self):
        return len(self.infos)
    
    
    def __getitem__(self, idx):
        # this includes the map_object for the the given sample idx?
        # only 1 map for a single scene. the idx doesn't affect the map.
        # create scene level data should return the 3 EGOs per sample
        ret_infos = self.create_scene_level_data(idx)
        # convert dictionary format just makes the dictionary suitable for the simpler MTR model
        data = self.convert_dictionary_format(ret_infos)
        return data
        
        # maps = torch.from_numpy(data['maps'])
        # hist_trajs = torch.from_numpy(data['hist_trajs'])
        # hist_valid = data['hist_valid']
        # fut_trajs = data['fut_gt_trajs']
        # fut_valid = data['fut_valid']

        # return {
        #     'hist_trajs': torch.from_numpy(data['hist_trajs']).float(),
        #     'maps': torch.from_numpy(data['maps']).float(),
        #     'fut_gt_trajs': torch.from_numpy(data['fut_gt_trajs']).float(),
        #     'hist_valid': torch.from_numpy(data['hist_valid']).float(),
        #     'fut_valid': torch.from_numpy(data['fut_valid']).float()
        # }
        
    def create_scene_level_data(self, index):
        """
        Args:
            index (index):

        Returns:

        """
        info = self.infos[index]
        scene_id = info['scenario_id']
        with open(self.data_path / f'sample_{scene_id}.pkl', 'rb') as f:
            info = pickle.load(f)

        sdc_track_index = info['sdc_track_index']
        current_time_index = info['current_time_index']
        timestamps = np.array(info['timestamps_seconds'][:current_time_index + 1], dtype=np.float32)

        track_infos = info['track_infos']

        track_index_to_predict = np.array(info['tracks_to_predict']['track_index'])
        obj_types = np.array(track_infos['object_type'])
        obj_ids = np.array(track_infos['object_id'])
        obj_trajs_full = track_infos['trajs']  # (num_objects, num_timestamp, 10)
        obj_trajs_past = obj_trajs_full[:, :current_time_index + 1]
        obj_trajs_future = obj_trajs_full[:, current_time_index + 1:]

        center_objects, track_index_to_predict = self.get_interested_agents(
            track_index_to_predict=track_index_to_predict,
            obj_trajs_full=obj_trajs_full,
            current_time_index=current_time_index,
            obj_types=obj_types, scene_id=scene_id
        )

        (obj_trajs_data, obj_trajs_mask, obj_trajs_pos, obj_trajs_last_pos, obj_trajs_future_state, obj_trajs_future_mask, center_gt_trajs,
            center_gt_trajs_mask, center_gt_final_valid_idx,
            track_index_to_predict_new, sdc_track_index_new, obj_types, obj_ids) = self.create_agent_data_for_center_objects(
            center_objects=center_objects, obj_trajs_past=obj_trajs_past, obj_trajs_future=obj_trajs_future,
            track_index_to_predict=track_index_to_predict, sdc_track_index=sdc_track_index,
            timestamps=timestamps, obj_types=obj_types, obj_ids=obj_ids
        )

        ret_dict = {
            'scenario_id': np.array([scene_id] * len(track_index_to_predict)),
            'obj_trajs': obj_trajs_data,
            'obj_trajs_mask': obj_trajs_mask,
            'track_index_to_predict': track_index_to_predict_new,  # used to select center-features
            'obj_trajs_pos': obj_trajs_pos,
            'obj_trajs_last_pos': obj_trajs_last_pos,
            'obj_types': obj_types,
            'obj_ids': obj_ids,

            'center_objects_world': center_objects,
            'center_objects_id': np.array(track_infos['object_id'])[track_index_to_predict],
            'center_objects_type': np.array(track_infos['object_type'])[track_index_to_predict],

            'obj_trajs_future_state': obj_trajs_future_state,
            'obj_trajs_future_mask': obj_trajs_future_mask,
            'center_gt_trajs': center_gt_trajs,
            'center_gt_trajs_mask': center_gt_trajs_mask,
            'center_gt_final_valid_idx': center_gt_final_valid_idx,
            'center_gt_trajs_src': obj_trajs_full[track_index_to_predict]
        }

        if not self.dataset_cfg['WITHOUT_HDMAP']:
            if info['map_infos']['all_polylines'].__len__() == 0:
                info['map_infos']['all_polylines'] = np.zeros((2, 7), dtype=np.float32)
                print(f'Warning: empty HDMap {scene_id}')
            
            map_tensor = self.create_map_data_for_center_objects(
            center_objects=center_objects, map_infos=info['map_infos'],
            center_offset=self.dataset_cfg['CENTER_OFFSET_OF_MAP'])   # (num_center_objects, num_topk_polylines, num_points_each_polyline, 9), (num_center_objects, num_topk_polylines, num_points_each_polyline)

            ret_dict['maps'] = map_tensor
            # map_polylines_data, map_polylines_mask, map_polylines_center = self.create_map_data_for_center_objects(
            #     center_objects=center_objects, map_infos=info['map_infos'],
            #     center_offset=self.dataset_cfg['CENTER_OFFSET_OF_MAP'])   # (num_center_objects, num_topk_polylines, num_points_each_polyline, 9), (num_center_objects, num_topk_polylines, num_points_each_polyline)

            # ret_dict['map_polylines'] = map_polylines_data
            # ret_dict['map_polylines_mask'] = (map_polylines_mask > 0)
            # ret_dict['map_polylines_center'] = map_polylines_center

        return ret_dict

    def create_agent_data_for_center_objects(
            self, center_objects, obj_trajs_past, obj_trajs_future, track_index_to_predict, sdc_track_index, timestamps,
            obj_types, obj_ids
        ):
        obj_trajs_data, obj_trajs_mask, obj_trajs_future_state, obj_trajs_future_mask = self.generate_centered_trajs_for_agents(
            center_objects=center_objects, obj_trajs_past=obj_trajs_past,
            obj_types=obj_types, center_indices=track_index_to_predict,
            sdc_index=sdc_track_index, timestamps=timestamps, obj_trajs_future=obj_trajs_future
        )

        # generate the labels of track_objects for training
        center_obj_idxs = np.arange(len(track_index_to_predict))
        center_gt_trajs = obj_trajs_future_state[center_obj_idxs, track_index_to_predict]  # (num_center_objects, num_future_timestamps, 4)
        center_gt_trajs_mask = obj_trajs_future_mask[center_obj_idxs, track_index_to_predict]  # (num_center_objects, num_future_timestamps)
        center_gt_trajs[center_gt_trajs_mask == 0] = 0

        # filter invalid past trajs
        assert obj_trajs_past.__len__() == obj_trajs_data.shape[1]
        valid_past_mask = np.logical_not(obj_trajs_past[:, :, -1].sum(axis=-1) == 0)  # (num_objects (original))

        obj_trajs_mask = obj_trajs_mask[:, valid_past_mask]  # (num_center_objects, num_objects (filtered), num_timestamps)
        obj_trajs_data = obj_trajs_data[:, valid_past_mask]  # (num_center_objects, num_objects (filtered), num_timestamps, C)
        obj_trajs_future_state = obj_trajs_future_state[:, valid_past_mask]  # (num_center_objects, num_objects (filtered), num_timestamps_future, 4):  [x, y, vx, vy]
        obj_trajs_future_mask = obj_trajs_future_mask[:, valid_past_mask]  # (num_center_objects, num_objects, num_timestamps_future):
        obj_types = obj_types[valid_past_mask]
        obj_ids = obj_ids[valid_past_mask]

        valid_index_cnt = valid_past_mask.cumsum(axis=0)
        track_index_to_predict_new = valid_index_cnt[track_index_to_predict] - 1
        sdc_track_index_new = valid_index_cnt[sdc_track_index] - 1  # TODO: CHECK THIS

        assert obj_trajs_future_state.shape[1] == obj_trajs_data.shape[1]
        assert len(obj_types) == obj_trajs_future_mask.shape[1]
        assert len(obj_ids) == obj_trajs_future_mask.shape[1]

        # generate the final valid position of each object
        obj_trajs_pos = obj_trajs_data[:, :, :, 0:3]
        num_center_objects, num_objects, num_timestamps, _ = obj_trajs_pos.shape
        obj_trajs_last_pos = np.zeros((num_center_objects, num_objects, 3), dtype=np.float32)
        for k in range(num_timestamps):
            cur_valid_mask = obj_trajs_mask[:, :, k] > 0  # (num_center_objects, num_objects)
            obj_trajs_last_pos[cur_valid_mask] = obj_trajs_pos[:, :, k, :][cur_valid_mask]

        center_gt_final_valid_idx = np.zeros((num_center_objects), dtype=np.float32)
        for k in range(center_gt_trajs_mask.shape[1]):
            cur_valid_mask = center_gt_trajs_mask[:, k] > 0  # (num_center_objects)
            center_gt_final_valid_idx[cur_valid_mask] = k

        return (obj_trajs_data, obj_trajs_mask > 0, obj_trajs_pos, obj_trajs_last_pos,
            obj_trajs_future_state, obj_trajs_future_mask, center_gt_trajs, center_gt_trajs_mask, center_gt_final_valid_idx,
            track_index_to_predict_new, sdc_track_index_new, obj_types, obj_ids)

    def get_interested_agents(self, track_index_to_predict, obj_trajs_full, current_time_index, obj_types, scene_id):
        center_objects_list = []
        track_index_to_predict_selected = []

        for k in range(len(track_index_to_predict)):
            obj_idx = track_index_to_predict[k]

            assert obj_trajs_full[obj_idx, current_time_index, -1] > 0, f'obj_idx={obj_idx}, scene_id={scene_id}'

            center_objects_list.append(obj_trajs_full[obj_idx, current_time_index])
            track_index_to_predict_selected.append(obj_idx)

        center_objects = np.stack(center_objects_list, axis=0)  # (num_center_objects, num_attrs)
        track_index_to_predict = np.array(track_index_to_predict_selected)
        return center_objects, track_index_to_predict

    @staticmethod
    def transform_trajs_to_center_coords(obj_trajs, center_xyz, center_heading, heading_index, rot_vel_index=None):
        """
        Args:
            obj_trajs (num_objects, num_timestamps, num_attrs):
                first three values of num_attrs are [x, y, z] or [x, y]
            center_xyz (num_center_objects, 3 or 2): [x, y, z] or [x, y]
            center_heading (num_center_objects):
            heading_index: the index of heading angle in the num_attr-axis of obj_trajs
        """
        num_objects, num_timestamps, num_attrs = obj_trajs.shape
        num_center_objects = center_xyz.shape[0]
        assert center_xyz.shape[0] == center_heading.shape[0]
        assert center_xyz.shape[1] in [3, 2]

        obj_trajs = obj_trajs.clone().view(1, num_objects, num_timestamps, num_attrs).repeat(num_center_objects, 1, 1, 1)
        obj_trajs[:, :, :, 0:center_xyz.shape[1]] -= center_xyz[:, None, None, :]
        obj_trajs[:, :, :, 0:2] = common_utils.rotate_points_along_z(
            points=obj_trajs[:, :, :, 0:2].view(num_center_objects, -1, 2),
            angle=-center_heading
        ).view(num_center_objects, num_objects, num_timestamps, 2)

        obj_trajs[:, :, :, heading_index] -= center_heading[:, None, None]

        # rotate direction of velocity
        if rot_vel_index is not None:
            assert len(rot_vel_index) == 2
            obj_trajs[:, :, :, rot_vel_index] = common_utils.rotate_points_along_z(
                points=obj_trajs[:, :, :, rot_vel_index].view(num_center_objects, -1, 2),
                angle=-center_heading
            ).view(num_center_objects, num_objects, num_timestamps, 2)

        return obj_trajs

    def generate_centered_trajs_for_agents(self, center_objects, obj_trajs_past, obj_types, center_indices, sdc_index, timestamps, obj_trajs_future):
        """[summary]

        Args:
            center_objects (num_center_objects, 10): [cx, cy, cz, dx, dy, dz, heading, vel_x, vel_y, valid]
            obj_trajs_past (num_objects, num_timestamps, 10): [cx, cy, cz, dx, dy, dz, heading, vel_x, vel_y, valid]
            obj_types (num_objects):
            center_indices (num_center_objects): the index of center objects in obj_trajs_past
            centered_valid_time_indices (num_center_objects), the last valid time index of center objects
            timestamps ([type]): [description]
            obj_trajs_future (num_objects, num_future_timestamps, 10): [cx, cy, cz, dx, dy, dz, heading, vel_x, vel_y, valid]
        Returns:
            ret_obj_trajs (num_center_objects, num_objects, num_timestamps, num_attrs):
            ret_obj_valid_mask (num_center_objects, num_objects, num_timestamps):
            ret_obj_trajs_future (num_center_objects, num_objects, num_timestamps_future, 4):  [x, y, vx, vy]
            ret_obj_valid_mask_future (num_center_objects, num_objects, num_timestamps_future):
        """
        assert obj_trajs_past.shape[-1] == 10
        assert center_objects.shape[-1] == 10
        num_center_objects = center_objects.shape[0]
        num_objects, num_timestamps, box_dim = obj_trajs_past.shape
        # transform to cpu torch tensor
        center_objects = torch.from_numpy(center_objects).float()
        obj_trajs_past = torch.from_numpy(obj_trajs_past).float()
        timestamps = torch.from_numpy(timestamps)

        # transform coordinates to the centered objects
        obj_trajs = self.transform_trajs_to_center_coords(
            obj_trajs=obj_trajs_past,
            center_xyz=center_objects[:, 0:3],
            center_heading=center_objects[:, 6],
            heading_index=6, rot_vel_index=[7, 8]
        )

        ## generate the attributes for each object
        object_onehot_mask = torch.zeros((num_center_objects, num_objects, num_timestamps, 5))
        object_onehot_mask[:, obj_types == 'TYPE_VEHICLE', :, 0] = 1
        object_onehot_mask[:, obj_types == 'TYPE_PEDESTRAIN', :, 1] = 1  # TODO: CHECK THIS TYPO
        object_onehot_mask[:, obj_types == 'TYPE_CYCLIST', :, 2] = 1
        object_onehot_mask[torch.arange(num_center_objects), center_indices, :, 3] = 1
        object_onehot_mask[:, sdc_index, :, 4] = 1

        object_time_embedding = torch.zeros((num_center_objects, num_objects, num_timestamps, num_timestamps + 1))
        object_time_embedding[:, :, torch.arange(num_timestamps), torch.arange(num_timestamps)] = 1
        object_time_embedding[:, :, torch.arange(num_timestamps), -1] = timestamps

        object_heading_embedding = torch.zeros((num_center_objects, num_objects, num_timestamps, 2))
        object_heading_embedding[:, :, :, 0] = np.sin(obj_trajs[:, :, :, 6])
        object_heading_embedding[:, :, :, 1] = np.cos(obj_trajs[:, :, :, 6])

        vel = obj_trajs[:, :, :, 7:9]  # (num_centered_objects, num_objects, num_timestamps, 2)
        vel_pre = torch.roll(vel, shifts=1, dims=2)
        acce = (vel - vel_pre) / 0.1  # (num_centered_objects, num_objects, num_timestamps, 2)
        acce[:, :, 0, :] = acce[:, :, 1, :]

        ret_obj_trajs = torch.cat((
            obj_trajs[:, :, :, 0:6], 
            object_onehot_mask,
            object_time_embedding, 
            object_heading_embedding,
            obj_trajs[:, :, :, 7:9], 
            acce,
        ), dim=-1)

        ret_obj_valid_mask = obj_trajs[:, :, :, -1]  # (num_center_obejcts, num_objects, num_timestamps)  # TODO: CHECK THIS, 20220322
        ret_obj_trajs[ret_obj_valid_mask == 0] = 0

        ##  generate label for future trajectories
        obj_trajs_future = torch.from_numpy(obj_trajs_future).float()
        obj_trajs_future = self.transform_trajs_to_center_coords(
            obj_trajs=obj_trajs_future,
            center_xyz=center_objects[:, 0:3],
            center_heading=center_objects[:, 6],
            heading_index=6, rot_vel_index=[7, 8]
        )
        ret_obj_trajs_future = obj_trajs_future[:, :, :, [0, 1, 7, 8]]  # (x, y, vx, vy)
        ret_obj_valid_mask_future = obj_trajs_future[:, :, :, -1]  # (num_center_obejcts, num_objects, num_timestamps_future)  # TODO: CHECK THIS, 20220322
        ret_obj_trajs_future[ret_obj_valid_mask_future == 0] = 0

        return ret_obj_trajs.numpy(), ret_obj_valid_mask.numpy(), ret_obj_trajs_future.numpy(), ret_obj_valid_mask_future.numpy()

    @staticmethod
    def generate_batch_polylines_from_map(polylines, point_sampled_interval=1, vector_break_dist_thresh=1.0, num_points_each_polyline=20):
        """
        Args:
            polylines (num_points, 7): [x, y, z, dir_x, dir_y, dir_z, global_type]

        Returns:
            ret_polylines: (num_polylines, num_points_each_polyline, 7)
            ret_polylines_mask: (num_polylines, num_points_each_polyline)
        """
        point_dim = polylines.shape[-1]

        sampled_points = polylines[::point_sampled_interval]
        sampled_points_shift = np.roll(sampled_points, shift=1, axis=0)
        buffer_points = np.concatenate((sampled_points[:, 0:2], sampled_points_shift[:, 0:2]), axis=-1) # [ed_x, ed_y, st_x, st_y]
        buffer_points[0, 2:4] = buffer_points[0, 0:2]

        break_idxs = (np.linalg.norm(buffer_points[:, 0:2] - buffer_points[:, 2:4], axis=-1) > vector_break_dist_thresh).nonzero()[0]
        polyline_list = np.array_split(sampled_points, break_idxs, axis=0)
        ret_polylines = []
        ret_polylines_mask = []

        def append_single_polyline(new_polyline):
            cur_polyline = np.zeros((num_points_each_polyline, point_dim), dtype=np.float32)
            cur_valid_mask = np.zeros((num_points_each_polyline), dtype=np.int32)
            cur_polyline[:len(new_polyline)] = new_polyline
            cur_valid_mask[:len(new_polyline)] = 1
            ret_polylines.append(cur_polyline)
            ret_polylines_mask.append(cur_valid_mask)

        for k in range(len(polyline_list)):
            if polyline_list[k].__len__() <= 0:
                continue
            for idx in range(0, len(polyline_list[k]), num_points_each_polyline):
                append_single_polyline(polyline_list[k][idx: idx + num_points_each_polyline])

        ret_polylines = np.stack(ret_polylines, axis=0)
        ret_polylines_mask = np.stack(ret_polylines_mask, axis=0)

        ret_polylines = torch.from_numpy(ret_polylines)
        ret_polylines_mask = torch.from_numpy(ret_polylines_mask)

        # # CHECK the results
        # polyline_center = ret_polylines[:, :, 0:2].sum(dim=1) / ret_polyline_valid_mask.sum(dim=1).float()[:, None]  # (num_polylines, 2)
        # center_dist = (polyline_center - ret_polylines[:, 0, 0:2]).norm(dim=-1)
        # assert center_dist.max() < 10
        return ret_polylines, ret_polylines_mask

    def create_map_data_for_center_objects(self, center_objects, map_infos, center_offset):
        """
        Args:
            center_objects (num_center_objects, 10): [cx, cy, cz, dx, dy, dz, heading, vel_x, vel_y, valid]
            map_infos (dict):
                all_polylines (num_points, 7): [x, y, z, dir_x, dir_y, dir_z, global_type]
            center_offset (2):, [offset_x, offset_y]
        Returns:
            map_polylines (num_center_objects, num_topk_polylines, num_points_each_polyline, 9): [x, y, z, dir_x, dir_y, dir_z, global_type, pre_x, pre_y]
            map_polylines_mask (num_center_objects, num_topk_polylines, num_points_each_polyline)
               # NEW: Return structured lane metadata
            map_lane_metadata: List[Dict] - one dict per center object
                Each dict contains:
                {
                    'lanes': List of lane dicts with entry/exit info,
                    'road_lines': List of road line dicts,
                    'polyline_to_original_idx': Mapping from topk index to original lane
                }
        """
        num_center_objects = center_objects.shape[0]

        # transform object coordinates by center objects
        def transform_to_center_coordinates(neighboring_polylines, neighboring_polyline_valid_mask):
            neighboring_polylines[:, :, :, 0:3] -= center_objects[:, None, None, 0:3]
            neighboring_polylines[:, :, :, 0:2] = common_utils.rotate_points_along_z(
                points=neighboring_polylines[:, :, :, 0:2].view(num_center_objects, -1, 2),
                angle=-center_objects[:, 6]
            ).view(num_center_objects, -1, batch_polylines.shape[1], 2)
            neighboring_polylines[:, :, :, 3:5] = common_utils.rotate_points_along_z(
                points=neighboring_polylines[:, :, :, 3:5].view(num_center_objects, -1, 2),
                angle=-center_objects[:, 6]
            ).view(num_center_objects, -1, batch_polylines.shape[1], 2)

            # use pre points to map
            # (num_center_objects, num_polylines, num_points_each_polyline, num_feat)
            xy_pos_pre = neighboring_polylines[:, :, :, 0:2]
            xy_pos_pre = torch.roll(xy_pos_pre, shifts=1, dims=-2)
            xy_pos_pre[:, :, 0, :] = xy_pos_pre[:, :, 1, :]
            neighboring_polylines = torch.cat((neighboring_polylines, xy_pos_pre), dim=-1)

            neighboring_polylines[neighboring_polyline_valid_mask == 0] = 0
            return neighboring_polylines, neighboring_polyline_valid_mask

    
        polylines = torch.from_numpy(map_infos['all_polylines'].copy())
        center_objects = torch.from_numpy(center_objects)

        batch_polylines, batch_polylines_mask = self.generate_batch_polylines_from_map(
            polylines=polylines.numpy(), point_sampled_interval=self.dataset_cfg['POINT_SAMPLED_INTERVAL'],
            vector_break_dist_thresh=self.dataset_cfg['VECTOR_BREAK_DIST_THRESH'],
            num_points_each_polyline=self.dataset_cfg['NUM_POINTS_EACH_POLYLINE'],
        )  # (num_polylines, num_points_each_polyline, 7), (num_polylines, num_points_each_polyline)

        # collect a number of closest polylines for each center objects
        num_of_src_polylines = self.dataset_cfg['NUM_OF_SRC_POLYLINES']

        if len(batch_polylines) > num_of_src_polylines:
            polyline_center = batch_polylines[:, :, 0:2].sum(dim=1) / torch.clamp_min(batch_polylines_mask.sum(dim=1).float()[:, None], min=1.0)
            center_offset_rot = torch.from_numpy(np.array(center_offset, dtype=np.float32))[None, :].repeat(num_center_objects, 1)
            center_offset_rot = common_utils.rotate_points_along_z(
                points=center_offset_rot.view(num_center_objects, 1, 2),
                angle=center_objects[:, 6]
            ).view(num_center_objects, 2)

            pos_of_map_centers = center_objects[:, 0:2] + center_offset_rot

            dist = (pos_of_map_centers[:, None, :] - polyline_center[None, :, :]).norm(dim=-1)  # (num_center_objects, num_polylines)
            topk_dist, topk_idxs = dist.topk(k=num_of_src_polylines, dim=-1, largest=False)
            map_polylines = batch_polylines[topk_idxs]  # (num_center_objects, num_topk_polylines, num_points_each_polyline, 7)
            map_polylines_mask = batch_polylines_mask[topk_idxs]  # (num_center_objects, num_topk_polylines, num_points_each_polyline)
        else:
            map_polylines = batch_polylines[None, :, :, :].repeat(num_center_objects, 1, 1, 1)
            map_polylines_mask = batch_polylines_mask[None, :, :].repeat(num_center_objects, 1, 1)

        map_polylines, map_polylines_mask = transform_to_center_coordinates(
            neighboring_polylines=map_polylines,
            neighboring_polyline_valid_mask=map_polylines_mask
        )

        temp_sum = (map_polylines[:, :, :, 0:3] * map_polylines_mask[:, :, :, None].float()).sum(dim=-2)  # (num_center_objects, num_polylines, 3)
        map_polylines_center = temp_sum / torch.clamp_min(map_polylines_mask.sum(dim=-1).float()[:, :, None], min=1.0)  # (num_center_objects, num_polylines, 3)

        map_polylines = map_polylines.numpy()
        map_polylines_mask = map_polylines_mask.numpy()
        map_polylines_center = map_polylines_center.numpy()
        
        # add some processing for getting the entry lane, exit lane, and left boundary, right boundary of the lanes
        # there seems to be 324 entry/exit lanes and left/right boundaries
        def convert_lane_type(type_str):
            """Convert MTR lane type to your LaneType enum."""
            type_map = {
                'TYPE_FREEWAY': LaneType.Driving,
                'TYPE_SURFACE_STREET': LaneType.Driving,
                'TYPE_BIKE_LANE': LaneType.Sidewalk,
            }
            return type_map.get(type_str, LaneType.Unknown)
        
        # Lane, Crosswalk, RoadLine, WalkButton -> Map
        # deal with lane
        map_features = []
        for lane in map_infos['lane']:
            # each lane is a dictionary
            start_polyline_index, end_polyline_index = lane['polyline_index']
            # polylines stores all_polylines
            geometry = polylines[start_polyline_index:end_polyline_index]
            # make sure that all_polylines consist of these 2D points
            polyline = [MapPoint(x=float(polyline[0]), y=float(polyline[1])) for polyline in geometry]
            road_id = lane['id']
            lane_id = lane['id']
            lane_type = convert_lane_type(lane['type'])
            # entry_lanes = [str(entry_lane) for entry_lane in lane['entry_lanes']]
            # exit_lanes = [str(exit_lane) for exit_lane in map_infos['exit_lanes']]
            # need to copy multiple left and right boundaries
            # left_boundary': [{'start_index': 0, 'end_index': 22, 'feature_id': 92, 'boundary_type': 0}]
            # 'right_boundary': [{'start_index': 0, 'end_index': 40, 'feature_id': 135, 'boundary_type': 'TYPE_UNKNOWN'}, {'start_index': 58, 'end_index': 72, 'feature_id': 135, 'boundary_type': 'TYPE_UNKNOWN'}]
            # skip boundary for now # TODO
            # left_boundary = map_infos['left_boundary']
            # left_start_index = left_boundary['start_index']
            # right_boundary = map_infos['right_boundary']
            lane_object = Lane(road_id=road_id, lane_id=lane_id, type=lane_type, polyline=polyline, entry_lanes=None, exit_lanes=None, boundary=None)
            map_features.append(lane_object)
            
        # deal with crosswalk
        # 'crosswalk': [{'id': 595, 'polyline_index': (26466, 26470)}, {'id': 596, 'polyline_index': (26470, 26474)}, {'id': 597, 'polyline_index': (26474, 26478)}
        for crosswalk in map_infos['crosswalk']:
            crosswalk_id = crosswalk['id']
            start_polyline_index, end_polyline_index = lane['polyline_index']
            # polylines stores all_polylines
            geometry = polylines[start_polyline_index:end_polyline_index]
            # make sure that all_polylines consist of these 2D points
            polyline = [MapPoint(x=float(polyline[0]), y=float(polyline[1])) for polyline in geometry]
            crosswalk_object = Crosswalk(polygon=polyline, id=crosswalk_id)
        
        # deal with roadline
        # 'road_line': [{'id': 1, 'type': 'TYPE_BROKEN_SINGLE_WHITE', 'polyline_index': (0, 141)}, {'id': 2, 'type': 'TYPE_BROKEN_SINGLE_WHITE', 'polyline_index': (141, 354)}
        for road_line in map_infos['road_line']:
            roadline_id = road_line['id']
            roadline_type = convert_lane_type(road_line['type'])
            start_polyline_index, end_polyline_index = road_line['polyline_index']
            # polylines stores all_polylines
            geometry = polylines[start_polyline_index:end_polyline_index]
            # make sure that all_polylines consist of these 2D points
            polyline = [MapPoint(x=float(polyline[0]), y=float(polyline[1])) for polyline in geometry]
            roadline_object = RoadLine(id=roadline_id, type=roadline_type, polyline=polyline)
            map_features.append(roadline_object)
        # return a Map object with no dynamic states and only map_features defined
        final_map_data = Map(map_features = map_features, dynamic_states = None)
        

        # inputs [B, M, W, 5] for map
        map_tensor = self.map_object_to_simple_model_input(final_map_data, max_polylines=256)
        
        return map_tensor # Returns ONE tensor, not per center


    def generate_prediction_dicts(self, batch_dict, output_path=None):
        """

        Args:
            batch_dict:
                pred_scores: (num_center_objects, num_modes)
                pred_trajs: (num_center_objects, num_modes, num_timestamps, 7)

              input_dict:
                center_objects_world: (num_center_objects, 10)
                center_objects_type: (num_center_objects)
                center_objects_id: (num_center_objects)
                center_gt_trajs_src: (num_center_objects, num_timestamps, 10)
        """
        input_dict = batch_dict['input_dict']

        pred_scores = batch_dict['pred_scores']
        pred_trajs = batch_dict['pred_trajs']
        center_objects_world = input_dict['center_objects_world'].type_as(pred_trajs)

        num_center_objects, num_modes, num_timestamps, num_feat = pred_trajs.shape
        assert num_feat == 7

        pred_trajs_world = common_utils.rotate_points_along_z(
            points=pred_trajs.view(num_center_objects, num_modes * num_timestamps, num_feat),
            angle=center_objects_world[:, 6].view(num_center_objects)
        ).view(num_center_objects, num_modes, num_timestamps, num_feat)
        pred_trajs_world[:, :, :, 0:2] += center_objects_world[:, None, None, 0:2]

        pred_dict_list = []
        batch_sample_count = batch_dict['batch_sample_count']
        start_obj_idx = 0
        for bs_idx in range(batch_dict['batch_size']):
            cur_scene_pred_list = []
            for obj_idx in range(start_obj_idx, start_obj_idx + batch_sample_count[bs_idx]):
                single_pred_dict = {
                    'scenario_id': input_dict['scenario_id'][obj_idx],
                    'pred_trajs': pred_trajs_world[obj_idx, :, :, 0:2].cpu().numpy(),
                    'pred_scores': pred_scores[obj_idx, :].cpu().numpy(),
                    'object_id': input_dict['center_objects_id'][obj_idx],
                    'object_type': input_dict['center_objects_type'][obj_idx],
                    'gt_trajs': input_dict['center_gt_trajs_src'][obj_idx].cpu().numpy(),
                    'track_index_to_predict': input_dict['track_index_to_predict'][obj_idx].cpu().numpy()
                }
                cur_scene_pred_list.append(single_pred_dict)

            pred_dict_list.append(cur_scene_pred_list)
            start_obj_idx += batch_sample_count[bs_idx]

        assert start_obj_idx == num_center_objects
        assert len(pred_dict_list) == batch_dict['batch_size']

        return pred_dict_list

    def evaluation(self, pred_dicts, output_path=None, eval_method='waymo', **kwargs):
        if eval_method == 'waymo':
            from .waymo_eval import waymo_evaluation
            try:
                num_modes_for_eval = pred_dicts[0][0]['pred_trajs'].shape[0]
            except:
                num_modes_for_eval = 6
            metric_results, result_format_str = waymo_evaluation(pred_dicts=pred_dicts, num_modes_for_eval=num_modes_for_eval)

            metric_result_str = '\n'
            for key in metric_results:
                metric_results[key] = metric_results[key]
                metric_result_str += '%s: %.4f \n' % (key, metric_results[key])
            metric_result_str += '\n'
            metric_result_str += result_format_str
        else:
            raise NotImplementedError

        return metric_result_str, metric_results

def collate_waymo_batch(batch_list):
    """
    Custom collate function for Waymo MTR-style dataset where:
      - Each sample contains multiple center objects (agents to predict)
      - All tensors already have fixed dimensions:
          hist_trajs:    (C, 5, 11, 6)
          maps:          (C, 256, 20, 5)
          fut_gt_trajs:  (C, 5, 80, 2)
          etc.
      - C = number of center objects in that scene (usually 1–3)

    This collate simply stacks along batch dimension after collecting all centers.
    """
    # batch_list should be dictionary
    hist_trajs = torch.cat([item['hist_trajs'] for item in batch_list], dim=0)
    hist_valid = torch.cat([item['hist_valid'] for item in batch_list], dim=0)
    fut_gt_trajs = torch.cat([item['fut_gt_trajs'] for item in batch_list], dim=0)
    fut_valid = torch.cat([item['fut_valid'] for item in batch_list], dim=0)
    maps = torch.cat([item['maps'] for item in batch_list], dim=0)
    
    return {
        'hist_trajs':     hist_trajs,      # [B, 5, 11, 6]
        'hist_valid':     hist_valid,      # [B, 5, 11]
        'fut_gt_trajs':   fut_gt_trajs,    # [B, 5, 80, 2]
        'fut_valid':      fut_valid,       # [B, 5, 80]
        'maps':           maps,            # [B, 256, 20, 5]
    }

# def collate_waymo_batch(batch_list):
#     """
#     Each item in batch_list has:
#       - hist_trajs: (3, 5, 11, 6)  # 3 centers
#       - maps: (256, 20, 5)          # shared map
#     """
#     batch_size = len(batch_list)
    
#     # Concatenate agent data (3 centers per sample)
#     hist_trajs = torch.cat([item['hist_trajs'] for item in batch_list], dim=0)  # (B*3, 5, 11, 6)
#     hist_valid = torch.cat([item['hist_valid'] for item in batch_list], dim=0)  # (B*3, 5, 11)
#     fut_gt_trajs = torch.cat([item['fut_gt_trajs'] for item in batch_list], dim=0)  # (B*3, 5, 80, 2)
#     fut_valid = torch.cat([item['fut_valid'] for item in batch_list], dim=0)  # (B*3, 5, 80)
    
#     # Stack maps (same for all samples, but need one per center object)
#     # Each sample has 3 centers, so repeat map 3 times per sample
#     maps = torch.stack([item['maps'] for item in batch_list], dim=0)  # (B, 256, 20, 5)
#     maps = maps.repeat_interleave(3, dim=0)  # (B*3, 256, 20, 5)
    
#     return {
#         'hist_trajs': hist_trajs,      # (B*3, 5, 11, 6)
#         'hist_valid': hist_valid,      # (B*3, 5, 11)
#         'fut_gt_trajs': fut_gt_trajs,  # (B*3, 5, 80, 2)
#         'fut_valid': fut_valid,        # (B*3, 5, 80)
#         'maps': maps,                  # (B*3, 256, 20, 5)
#     }
    
def collate_batch(batch_list):
    """
    Args:
    batch_list:
        scenario_id: (num_center_objects)
        track_index_to_predict (num_center_objects):

        obj_trajs (num_center_objects, num_objects, num_timestamps, num_attrs):
        obj_trajs_mask (num_center_objects, num_objects, num_timestamps):
        map_polylines (num_center_objects, num_polylines, num_points_each_polyline, 9): [x, y, z, dir_x, dir_y, dir_z, global_type, pre_x, pre_y]
        map_polylines_mask (num_center_objects, num_polylines, num_points_each_polyline)

        obj_trajs_pos: (num_center_objects, num_objects, num_timestamps, 3)
        obj_trajs_last_pos: (num_center_objects, num_objects, 3)
        obj_types: (num_objects)
        obj_ids: (num_objects)

        center_objects_world: (num_center_objects, 10)  [cx, cy, cz, dx, dy, dz, heading, vel_x, vel_y, valid]
        center_objects_type: (num_center_objects)
        center_objects_id: (num_center_objects)

        obj_trajs_future_state (num_center_objects, num_objects, num_future_timestamps, 4): [x, y, vx, vy]
        obj_trajs_future_mask (num_center_objects, num_objects, num_future_timestamps):
        center_gt_trajs (num_center_objects, num_future_timestamps, 4): [x, y, vx, vy]
        center_gt_trajs_mask (num_center_objects, num_future_timestamps):
        center_gt_final_valid_idx (num_center_objects): the final valid timestamp in num_future_timestamps
    """
    batch_size = len(batch_list)
    key_to_list = {}
    for key in batch_list[0].keys():
        key_to_list[key] = [batch_list[bs_idx][key] for bs_idx in range(batch_size)]

    input_dict = {}
    for key, val_list in key_to_list.items():

        if key in ['obj_trajs', 'obj_trajs_mask', 'map_polylines', 'map_polylines_mask', 'map_polylines_center',
            'obj_trajs_pos', 'obj_trajs_last_pos', 'obj_trajs_future_state', 'obj_trajs_future_mask']:
            val_list = [torch.from_numpy(x) for x in val_list]
            input_dict[key] = common_utils.merge_batch_by_padding_2nd_dim(val_list)
        elif key in ['scenario_id', 'obj_types', 'obj_ids', 'center_objects_type', 'center_objects_id']:
            input_dict[key] = np.concatenate(val_list, axis=0)
        else:
            val_list = [torch.from_numpy(x) for x in val_list]
            input_dict[key] = torch.cat(val_list, dim=0)

    batch_sample_count = [len(x['track_index_to_predict']) for x in batch_list]
    batch_dict = {'batch_size': batch_size, 'input_dict': input_dict, 'batch_sample_count': batch_sample_count}
    return batch_dict




def batch_nms(pred_trajs, pred_scores, dist_thresh=3, num_ret_modes=6):
    """
    Args:
        pred_trajs (batch_size, num_modes, num_timestamps, 2)
        pred_scores (batch_size, num_modes):
        dist_thresh (float):
        num_ret_modes (int, optional): Defaults to 6.

    Returns:
        ret_trajs (batch_size, num_ret_modes, num_timestamps, 2)
        ret_scores (batch_size, num_ret_modes)
        ret_idxs (batch_size, num_ret_modes)
    """
    batch_size, num_modes, num_timestamps, num_feat_dim = pred_trajs.shape

    sorted_idxs = pred_scores.argsort(dim=-1, descending=True)
    bs_idxs_full = torch.arange(batch_size).type_as(sorted_idxs)[:, None].repeat(1, num_modes)
    sorted_pred_scores = pred_scores[bs_idxs_full, sorted_idxs]
    sorted_pred_trajs = pred_trajs[bs_idxs_full, sorted_idxs]  # (batch_size, num_modes, num_timestamps, 7)
    sorted_pred_goals = sorted_pred_trajs[:, :, -1, :]  # (batch_size, num_modes, 7)

    dist = (sorted_pred_goals[:, :, None, 0:2] - sorted_pred_goals[:, None, :, 0:2]).norm(dim=-1)
    point_cover_mask = (dist < dist_thresh)

    point_val = sorted_pred_scores.clone()  # (batch_size, N)
    point_val_selected = torch.zeros_like(point_val)  # (batch_size, N)

    ret_idxs = sorted_idxs.new_zeros(batch_size, num_ret_modes).long()
    ret_trajs = sorted_pred_trajs.new_zeros(batch_size, num_ret_modes, num_timestamps, num_feat_dim)
    ret_scores = sorted_pred_trajs.new_zeros(batch_size, num_ret_modes)
    bs_idxs = torch.arange(batch_size).type_as(ret_idxs)

    for k in range(num_ret_modes):
        cur_idx = point_val.argmax(dim=-1) # (batch_size)
        ret_idxs[:, k] = cur_idx

        new_cover_mask = point_cover_mask[bs_idxs, cur_idx]  # (batch_size, N)
        point_val = point_val * (~new_cover_mask).float()  # (batch_size, N)
        point_val_selected[bs_idxs, cur_idx] = -1
        point_val += point_val_selected

        ret_trajs[:, k] = sorted_pred_trajs[bs_idxs, cur_idx]
        ret_scores[:, k] = sorted_pred_scores[bs_idxs, cur_idx]

    bs_idxs = torch.arange(batch_size).type_as(sorted_idxs)[:, None].repeat(1, num_ret_modes)

    ret_idxs = sorted_idxs[bs_idxs, ret_idxs]

    return ret_trajs, ret_scores, ret_idxs


def collate_waymo_data_old(batch):
    """
    Collate function for Waymo dataset with variable numbers of agents/polylines
    """
    batch_size = len(batch)
    
    # Find max dimensions
    max_agents = max(item['hist_trajs'].shape[0] for item in batch)
    max_polylines = max(item['maps'].shape[0] for item in batch)
    
    # Pad and collect
    hist_trajs_list = []
    fut_gt_trajs_list = []
    hist_valid_list = []
    fut_valid_list = []
    maps_list = []
    
    for item in batch:
        num_agents = item['hist_trajs'].shape[0]
        num_polylines = item['maps'].shape[0]
        
        agent_pad = max_agents - num_agents
        polyline_pad = max_polylines - num_polylines
        
        # Pad agents dimension for trajectory data
        hist_trajs_list.append(
            F.pad(item['hist_trajs'], (0, 0, 0, 0, 0, agent_pad), value=0)
        )
        fut_gt_trajs_list.append(
            F.pad(item['fut_gt_trajs'], (0, 0, 0, 0, 0, agent_pad), value=0)
        )
        hist_valid_list.append(
            F.pad(item['hist_valid'], (0, 0, 0, agent_pad), value=0)
        )
        fut_valid_list.append(
            F.pad(item['fut_valid'], (0, 0, 0, agent_pad), value=0)
        )
        
        # Pad polylines dimension for map data
        maps_list.append(
            F.pad(item['maps'], (0, 0, 0, 0, 0, polyline_pad), value=0)
        )
    
    # Stack into batch
    return {
        'hist_trajs': torch.stack(hist_trajs_list),
        'fut_gt_trajs': torch.stack(fut_gt_trajs_list),
        'hist_valid': torch.stack(hist_valid_list),
        'fut_valid': torch.stack(fut_valid_list),
        'maps': torch.stack(maps_list)
    }