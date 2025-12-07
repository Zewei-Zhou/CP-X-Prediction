import yaml
import torch
import random
import pickle
import glob
import numpy as np
from torch.utils.data import Dataset


def load_config(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    return data


class ChallengeDataset(Dataset):
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
        maps = data['maps']
        hist_trajs = data['hist_trajs']
        hist_valid = data['hist_valid']
        fut_trajs = data['fut_gt_trajs']
        fut_valid = data['fut_valid']

        inputs = {'hist_trajs': hist_trajs, 'maps': maps, 
                  'hist_valid': hist_valid, 'fut_gt_trajs': fut_trajs, 
                  'fut_valid': fut_valid}

        return inputs
    

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
    