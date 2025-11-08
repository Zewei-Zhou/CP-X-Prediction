import yaml
import torch
import random
import pickle
import glob
import numpy as np
from torch.utils.data import Dataset
import torch.nn.functional as F
# from torch.nn.utils.rnn import pad_sequence


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
    def __init__(self, data_path):
        self.data_list = []
        for path in data_path:
            self.data_list += glob.glob(path + '/*.pkl')

        self.history_timesteps = 11
        
    def load_data(self, data_path):
        with open(data_path, 'rb') as file:
            data = pickle.load(file)
            
        return data
    
    def __len__(self):
        return len(self.data_list)
    
    def __getitem__(self, idx):
        data = self.load_data(self.data_list[idx])
        # maps = torch.from_numpy(data['maps'])
        # hist_trajs = torchdata['hist_trajs']
        # hist_valid = data['hist_valid']
        # fut_trajs = data['fut_gt_trajs']
        # fut_valid = data['fut_valid']

        return {
            'hist_trajs': torch.from_numpy(data['hist_trajs']).to(torch.float16),
            'maps': torch.from_numpy(data['maps']).float(),
            'fut_gt_trajs': torch.from_numpy(data['fut_gt_trajs'],
            'hist_valid': torch.from_numpy(data['hist_valid']).float(),
            'fut_valid': torch.from_numpy(data['fut_valid']).float()
        }
    
    

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

# def collate_waymo_data(get_item_values):
#     # input is a batch size of getitem dictionaries, in this case there are 128 batches
#     # list of 128 dictionaries containing 5 keys
#     #   def __getitem__(self, idx):
#     #     data = self.load_data(self.data_list[idx])
#     #     maps = data['maps']
#     #     hist_trajs = data['hist_trajs']
#     #     hist_valid = data['hist_valid']
#     #     fut_trajs = data['fut_gt_trajs']
#     #     fut_valid = data['fut_valid']

#     #     inputs = {'hist_trajs': hist_trajs, 'maps': maps, 
#     #               'hist_valid': hist_valid, 'fut_gt_trajs': fut_trajs, 
#     #               'fut_valid': fut_valid}
        
#     #     return inputs
#     keys = list(get_item_values[0].keys())
#     final_collated_tensor_dict = {}
#     if keys != ['hist_trajs', 'maps', 'hist_valid', 'fut_gt_trajs', 'fut_valid']:
#         raise ValueError(f"Unexpected keys in get_item_values: {keys}")
#     for key in get_item_values:
#         current_key_batch_values = []
#         current_key_batch_values_tensors = []
#         for i in range(len(get_item_values)):
#             current_key_batch_values.append(get_item_values[i][key])
#         # find index of longest subarray within array of arrays
#         pad_length = len(max(current_key_batch_values, key=len))
#         for j in range(len(get_item_values)):
#             padded_tensor = F.pad(input = current_key_batch_values[j], pad = (0, pad_length), 
#                                 mode = "constant", value=0)
#             current_key_batch_values_tensors.append(padded_tensor)
#         tensorized_batch_key = torch.stack(current_key_batch_values_tensors, dim=0)
#         final_collated_tensor_dict[key] = tensorized_batch_key
#     return final_collated_tensor_dict
    
def collate_waymo_data(batch):
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