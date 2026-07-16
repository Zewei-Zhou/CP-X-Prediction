# %%
import sys
import os
import pickle
import torch
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.transforms import Affine2D
from sklearn.cluster import KMeans

# Path adjustments based on your original script
sys.path.insert(0, "/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Prediction/MTR")
sys.path.append('../../map/')
sys.path.insert(0, "/data/robert/CP-X-Prediction/V2XPnP_dev/opencood")
from mtr.datasets.waymo.waymo_dataset import *
from map import *
from map_types import *

# %%
# ---------------------------------------------------------
# 1. LOAD TEST RESULTS
# ---------------------------------------------------------
test_results_path = '/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Prediction/MTR/output/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Prediction/MTR/tools/cfgs/challenge/mtr-finetuning-full-map-testing-V2XPNP/default/eval/epoch_30/default/result.pkl'
with open(test_results_path, 'rb') as file:
    test_results = pickle.load(file)

output_test_results = "/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Visualization/cpx_mtr_viz/test_results.txt"
os.makedirs(os.path.dirname(output_test_results), exist_ok=True)
with open(output_test_results, "w") as f:
    print(test_results[0][0], file=f)
    print(test_results[0][0].keys(), file=f)
    print(len(test_results), file=f)
    print(test_results[0][0]['pred_trajs'].shape, file=f)  # (6 modes, 80 timesteps, 2 coordinates)

print(f"Number of agents for the first scene: {len(test_results[0])}")
print(f"Number of dictionary keys: {len(test_results[0][0])}")
print(f"Shape of predicted trajs: {str(test_results[0][0]['pred_trajs'].shape)}")

is_same_scene = test_results[0][0]['scenario_id'] == test_results[0][1]['scenario_id']
print(f"Are the first two agents from the same scene? {is_same_scene}")


# %%
# ---------------------------------------------------------
# 2. PLOTTING FUNCTIONS
# ---------------------------------------------------------
def plot_traj(sample_id, traj_id, data, mode):
    pred_traj = data[sample_id][traj_id]['pred_trajs']
    gt_traj = data[sample_id][traj_id]['gt_trajs']
    
    for i in range(mode):
        pred_traj_i = pred_traj[i]
        x_coords = np.insert(pred_traj_i[:, 0], 0, gt_traj[10, 0])
        y_coords = np.insert(pred_traj_i[:, 1], 0, gt_traj[10, 1])
        plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='red', markersize=1)

    plt.plot(gt_traj[:, 0], gt_traj[:, 1], marker='o', linestyle='-', color='blue', markersize=1)
    plt.plot(gt_traj[:11, 0], gt_traj[:11, 1], marker='o', linestyle='-', color='green', markersize=1)
    plt.plot(gt_traj[10][0], gt_traj[10][1], marker='*', color='yellow', markersize=5)
    plt.show()

def plot_v2xpnp_map(map_object, ax):
    """Plot map features. Uses duck typing so pickles from opencood match (type() != local Lane)."""
    for map_feature in map_object.map_features:
        if getattr(map_feature, "polyline", None):
            pts = map_feature.polyline
            x = [p.x for p in pts]
            y = [p.y for p in pts]
            if len(x) >= 2:
                ax.plot(x, y, color="k", alpha=0.5, linewidth=0.8, zorder=1)
            elif len(x) == 1:
                ax.plot(x, y, color="k", marker=".", markersize=2, alpha=0.5, zorder=1)
        elif getattr(map_feature, "polygon", None):
            pts = map_feature.polygon
            x = [p.x for p in pts]
            y = [p.y for p in pts]
            if len(x) >= 2:
                if x[0] != x[-1] or y[0] != y[-1]:
                    x, y = x + [x[0]], y + [y[0]]
                ax.plot(x, y, color="k", alpha=0.5, linewidth=0.8, zorder=1)
        elif getattr(map_feature, "position", None):
            p = map_feature.position
            ax.plot([p.x], [p.y], color="k", marker=".", markersize=3, alpha=0.6, zorder=1)

def plot_entire_project_map(ax):
    corridors_map = "/data/dataset/v2x-real-pnp/map/v2v_corridors_vector_map.pkl"
    intersection_map = "/data/dataset/v2x-real-pnp/map/v2x_intersection_vector_map.pkl"
    
    with open(corridors_map, 'rb') as f:
        corridors_map_object = pickle.load(f)
        
    with open(intersection_map, 'rb') as f:
        intersection_map_object = pickle.load(f)
        
    plot_v2xpnp_map(corridors_map_object, ax)
    plot_v2xpnp_map(intersection_map_object, ax)
    
        
def plot_traj_withmap_withheading_specific(sample_id, data, vector_map, mode):
    # --- 0. Pre-Calculation of Scene Statistics (WITH MASKING) ---
    scene_agents = data[sample_id]
    scenario_id = scene_agents[0].get('scenario_id', 'Unknown')
    
    total_min_ade, total_min_fde, valid_agents_count = 0, 0, 0

    for agent in scene_agents:
        gt_traj = agent['gt_trajs']
        gt_future = gt_traj[10:, :2] 
        
        # Identify valid frames (not 0,0 padding)
        mask = (gt_future[:, 0] != 0) | (gt_future[:, 1] != 0)
        if np.sum(mask) == 0:
            continue

        pred_trajs = agent['pred_trajs']
        pred_scores = agent['pred_scores']
        
        top_indices = np.argsort(pred_scores)[-mode:][::-1]
        top_preds = pred_trajs[top_indices]

        agent_ades, agent_fdes = [], []
        
        for k in range(mode):
            pred_future = top_preds[k][:, :2]
            min_len = min(len(gt_future), len(pred_future))
            valid_mask = mask[:min_len]
            
            if np.sum(valid_mask) > 0:
                diff = gt_future[:min_len] - pred_future[:min_len]
                l2_dist = np.linalg.norm(diff, axis=1)
                valid_l2 = l2_dist[valid_mask]
                
                agent_ades.append(np.mean(valid_l2))
                agent_fdes.append(valid_l2[-1])
            else:
                agent_ades.append(9999.0)
                agent_fdes.append(9999.0)
        
        if agent_ades:
            best_ade = min(agent_ades)
            if best_ade < 9999.0:
                total_min_ade += best_ade
                total_min_fde += min(agent_fdes)
                valid_agents_count += 1

    avg_ade = total_min_ade / valid_agents_count if valid_agents_count > 0 else 0
    avg_fde = total_min_fde / valid_agents_count if valid_agents_count > 0 else 0

    print(f"--- Scene Stats (ID: {sample_id}) ---")
    print(f"Valid Agents: {valid_agents_count}")
    print(f"Scene minADE: {avg_ade:.4f}")
    print(f"Scene minFDE: {avg_fde:.4f}")

    # --- 1. Setup Plot ---
    fig, ax = plt.subplots()
    fig.set_size_inches(20, 25)
    legend_added = {}

    # --- 2. Plot Map Features ---
    plot_entire_project_map(ax)
    # for feature in vector_map.map_features:
    #     if isinstance(feature, Lane):
    #         if feature.type == LaneType.Sidewalk:
    #             label = "Sidewalk" if "Sidewalk" not in legend_added else ""
    #             ax.plot([p.x for p in feature.polyline], [p.y for p in feature.polyline], 
    #                     'k--', linewidth=1, alpha=0.5, label=label)
    #             legend_added["Sidewalk"] = True
    #         elif feature.type == LaneType.Shoulder:
    #             continue
    #         else:
    #             label = "Lane" if "Lane" not in legend_added else ""
    #             ax.plot([p.x for p in feature.polyline], [p.y for p in feature.polyline], 
    #                     'k', linewidth=1, alpha=0.3, label=label)
    #             legend_added["Lane"] = True
    #     elif isinstance(feature, Crosswalk):
    #         label = "Crosswalk" if "Crosswalk" not in legend_added else ""
    #         polygon = feature.polygon
    #         ax.plot([p.x for p in polygon], [p.y for p in polygon], 
    #                 'k', linewidth=1, alpha=0.5, label=label)
    #         legend_added["Crosswalk"] = True
    #     elif isinstance(feature, RoadLine):
    #         ax.plot([p.x for p in feature.polyline], [p.y for p in feature.polyline], 'k', alpha=0.5)

    # --- 3. Iterate Agents ---
    for traj_id in range(len(scene_agents)):
        agent_data = scene_agents[traj_id]
        object_type = agent_data['object_type']
        
        pred_traj = agent_data['pred_trajs']
        gt_traj = agent_data['gt_trajs']
        pred_scores = agent_data['pred_scores']
        
        top3_indices = np.argsort(pred_scores)[-mode:][::-1]
        top3_pred_trajs = pred_traj[top3_indices]
        top3_scores = pred_scores[top3_indices]

        curr_x, curr_y = gt_traj[10][0], gt_traj[10][1]
        heading = gt_traj[10][6] 

        # Colors & Shapes
        if object_type == "TYPE_VEHICLE":
            agent_color, history_color, label_name = 'cyan', 'dodgerblue', "Vehicle"
            # Center-relative box + Affine2D (works on matplotlib < 3.8; no rotation_point kwarg)
            vehicle_transform = (
                Affine2D().rotate_deg(np.degrees(heading)).translate(curr_x, curr_y)
                + ax.transData
            )
            shape_patch = patches.Rectangle(
                (-2.25, -1.0), 4.5, 2.0, transform=vehicle_transform,
                edgecolor='black', facecolor=agent_color, alpha=0.9, zorder=5,
            )
        elif object_type == "TYPE_PEDESTRIAN":
            agent_color, history_color, label_name = 'orange', 'tomato', "Pedestrian"
            shape_patch = patches.Circle((curr_x, curr_y), radius=0.6, 
                                         edgecolor='black', facecolor=agent_color, alpha=0.9, zorder=5)
        elif object_type == "TYPE_CYCLIST":
            agent_color, history_color, label_name = 'lime', 'darkgreen', "Cyclist"
            shape_patch = patches.RegularPolygon((curr_x, curr_y), numVertices=3, radius=1.2, 
                                                 orientation=heading, edgecolor='black',
                                                 facecolor=agent_color, alpha=0.9, zorder=5)
        else:
            agent_color, history_color, label_name = 'yellow', 'goldenrod', "Unknown"
            shape_patch = patches.Circle((curr_x, curr_y), radius=0.5, color=agent_color)

        current_label = label_name if label_name not in legend_added else ""
        if current_label: 
            legend_added[label_name] = True
            ax.plot([], [], color=agent_color, marker='o', label=current_label, linestyle='None')

        ax.add_patch(shape_patch)

        # Plot History
        hist_x, hist_y = gt_traj[:11, 0], gt_traj[:11, 1]
        hist_mask = (hist_x != 0) | (hist_y != 0)
        ax.plot(hist_x[hist_mask], hist_y[hist_mask], color=history_color, linewidth=1.5, linestyle='-', alpha=0.7, zorder=3)
        
        # Plot GT Future
        fut_x, fut_y = gt_traj[10:, 0], gt_traj[10:, 1]
        fut_mask = (fut_x != 0) | (fut_y != 0)
        ax.plot(fut_x[fut_mask], fut_y[fut_mask], color=agent_color, linewidth=2, linestyle='-', alpha=0.8, zorder=4)

        # Plot Predictions
        for i in range(mode):
            pred_traj_i = top3_pred_trajs[i]
            px, py = np.insert(pred_traj_i[:, 0], 0, curr_x), np.insert(pred_traj_i[:, 1], 0, curr_y)
            p_mask = (px != 0) | (py != 0)
            
            is_best = (i == 0)
            lw = 1.5 if is_best else 0.5
            ax.plot(px[p_mask], py[p_mask], color=agent_color, linestyle='--', linewidth=lw, alpha=0.6)

            if is_best:
                score_str = f"{top3_scores[i]:.2f}"
                ax.text(curr_x + 1.5, curr_y + 1.5, score_str, color='black', fontsize=9, fontweight='bold',
                        bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=0.2), zorder=7)

    stats_text = f"Scenario ID: {scenario_id}\nminADE: {avg_ade:.2f}m\nminFDE: {avg_fde:.2f}m"
    ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'))

    ax.set_aspect('equal')
    ax.legend(loc='upper right')
    plt.title(f"Trajectory Prediction Visualization - Sample {sample_id}")
    plt.tight_layout()
    
    save_dir = "/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Visualization/plots/finetune_project_validation"
    os.makedirs(save_dir, exist_ok=True)
    plt.savefig(os.path.join(save_dir, f"scenario_{sample_id}_{scenario_id}.png"), dpi=150, bbox_inches='tight')
    plt.close()


# def plot_traj_withmap_withheading_specific(sample_id, data, vector_map, mode):
#     # --- 0. Pre-Calculation of Scene Statistics (WITH MASKING) ---
#     scene_agents = data[sample_id]
#     scenario_id = scene_agents[0].get('scenario_id', 'Unknown')
    
#     total_min_ade, total_min_fde, valid_agents_count = 0, 0, 0

#     for agent in scene_agents:
#         gt_traj = agent['gt_trajs']
#         gt_future = gt_traj[10:, :2] 
        
#         # Identify valid frames (not 0,0 padding)
#         mask = (gt_future[:, 0] != 0) | (gt_future[:, 1] != 0)
#         if np.sum(mask) == 0:
#             continue

#         pred_trajs = agent['pred_trajs']
#         pred_scores = agent['pred_scores']
        
#         top_indices = np.argsort(pred_scores)[-mode:][::-1]
#         top_preds = pred_trajs[top_indices]

#         agent_ades, agent_fdes = [], []
        
#         for k in range(mode):
#             pred_future = top_preds[k][:, :2]
#             min_len = min(len(gt_future), len(pred_future))
#             valid_mask = mask[:min_len]
            
#             if np.sum(valid_mask) > 0:
#                 diff = gt_future[:min_len] - pred_future[:min_len]
#                 l2_dist = np.linalg.norm(diff, axis=1)
#                 valid_l2 = l2_dist[valid_mask]
                
#                 agent_ades.append(np.mean(valid_l2))
#                 agent_fdes.append(valid_l2[-1])
#             else:
#                 agent_ades.append(9999.0)
#                 agent_fdes.append(9999.0)
        
#         if agent_ades:
#             best_ade = min(agent_ades)
#             if best_ade < 9999.0:
#                 total_min_ade += best_ade
#                 total_min_fde += min(agent_fdes)
#                 valid_agents_count += 1

#     avg_ade = total_min_ade / valid_agents_count if valid_agents_count > 0 else 0
#     avg_fde = total_min_fde / valid_agents_count if valid_agents_count > 0 else 0

#     print(f"--- Scene Stats (ID: {sample_id}) ---")
#     print(f"Valid Agents: {valid_agents_count}")
#     print(f"Scene minADE: {avg_ade:.4f}")
#     print(f"Scene minFDE: {avg_fde:.4f}")

#     # --- 1. Setup Plot ---
#     fig, ax = plt.subplots()
#     fig.set_size_inches(20, 25)
#     legend_added = {}

#     # --- 2. Plot Map Features ---
#     for feature in vector_map.map_features:
#         if isinstance(feature, Lane):
#             if feature.type == LaneType.Sidewalk:
#                 label = "Sidewalk" if "Sidewalk" not in legend_added else ""
#                 ax.plot([p.x for p in feature.polyline], [p.y for p in feature.polyline], 
#                         'k--', linewidth=1, alpha=0.5, label=label)
#                 legend_added["Sidewalk"] = True
#             elif feature.type == LaneType.Shoulder:
#                 continue
#             else:
#                 label = "Lane" if "Lane" not in legend_added else ""
#                 ax.plot([p.x for p in feature.polyline], [p.y for p in feature.polyline], 
#                         'k', linewidth=1, alpha=0.3, label=label)
#                 legend_added["Lane"] = True
#         elif isinstance(feature, Crosswalk):
#             label = "Crosswalk" if "Crosswalk" not in legend_added else ""
#             polygon = feature.polygon
#             ax.plot([p.x for p in polygon], [p.y for p in polygon], 
#                     'k', linewidth=1, alpha=0.5, label=label)
#             legend_added["Crosswalk"] = True
#         elif isinstance(feature, RoadLine):
#             ax.plot([p.x for p in feature.polyline], [p.y for p in feature.polyline], 'k', alpha=0.5)

#     # --- 3. Iterate Agents ---
#     for traj_id in range(len(scene_agents)):
#         agent_data = scene_agents[traj_id]
#         object_type = agent_data['object_type']
        
#         pred_traj = agent_data['pred_trajs']
#         gt_traj = agent_data['gt_trajs']
#         pred_scores = agent_data['pred_scores']
        
#         top3_indices = np.argsort(pred_scores)[-mode:][::-1]
#         top3_pred_trajs = pred_traj[top3_indices]
#         top3_scores = pred_scores[top3_indices]

#         curr_x, curr_y = gt_traj[10][0], gt_traj[10][1]
#         heading = gt_traj[10][6] 

#         # Colors & Shapes
#         if object_type == "TYPE_VEHICLE":
#             agent_color, history_color, label_name = 'cyan', 'dodgerblue', "Vehicle"
#             vehicle_transform = (
#                 Affine2D().rotate_deg(np.degrees(heading)).translate(curr_x, curr_y)
#                 + ax.transData
#             )
#             shape_patch = patches.Rectangle(
#                 (-2.25, -1.0), 4.5, 2.0, transform=vehicle_transform,
#                 edgecolor='black', facecolor=agent_color, alpha=0.9, zorder=5,
#             )
#         elif object_type == "TYPE_PEDESTRIAN":
#             agent_color, history_color, label_name = 'orange', 'tomato', "Pedestrian"
#             shape_patch = patches.Circle((curr_x, curr_y), radius=0.6, 
#                                          edgecolor='black', facecolor=agent_color, alpha=0.9, zorder=5)
#         elif object_type == "TYPE_CYCLIST":
#             agent_color, history_color, label_name = 'lime', 'darkgreen', "Cyclist"
#             shape_patch = patches.RegularPolygon((curr_x, curr_y), numVertices=3, radius=1.2, 
#                                                  orientation=heading, edgecolor='black',
#                                                  facecolor=agent_color, alpha=0.9, zorder=5)
#         else:
#             agent_color, history_color, label_name = 'yellow', 'goldenrod', "Unknown"
#             shape_patch = patches.Circle((curr_x, curr_y), radius=0.5, color=agent_color)

#         current_label = label_name if label_name not in legend_added else ""
#         if current_label: 
#             legend_added[label_name] = True
#             ax.plot([], [], color=agent_color, marker='o', label=current_label, linestyle='None')

#         ax.add_patch(shape_patch)

#         # Plot History
#         hist_x, hist_y = gt_traj[:11, 0], gt_traj[:11, 1]
#         hist_mask = (hist_x != 0) | (hist_y != 0)
#         ax.plot(hist_x[hist_mask], hist_y[hist_mask], color=history_color, linewidth=1.5, linestyle='-', alpha=0.7, zorder=3)
        
#         # Plot GT Future
#         fut_x, fut_y = gt_traj[10:, 0], gt_traj[10:, 1]
#         fut_mask = (fut_x != 0) | (fut_y != 0)
#         ax.plot(fut_x[fut_mask], fut_y[fut_mask], color=agent_color, linewidth=2, linestyle='-', alpha=0.8, zorder=4)

#         # Plot Predictions
#         for i in range(mode):
#             pred_traj_i = top3_pred_trajs[i]
#             px, py = np.insert(pred_traj_i[:, 0], 0, curr_x), np.insert(pred_traj_i[:, 1], 0, curr_y)
#             p_mask = (px != 0) | (py != 0)
            
#             is_best = (i == 0)
#             lw = 1.5 if is_best else 0.5
#             ax.plot(px[p_mask], py[p_mask], color=agent_color, linestyle='--', linewidth=lw, alpha=0.6)

#             if is_best:
#                 score_str = f"{top3_scores[i]:.2f}"
#                 ax.text(curr_x + 1.5, curr_y + 1.5, score_str, color='black', fontsize=9, fontweight='bold',
#                         bbox=dict(facecolor='white', alpha=0.6, edgecolor='none', pad=0.2), zorder=7)

#     stats_text = f"Scenario ID: {scenario_id}\nminADE: {avg_ade:.2f}m\nminFDE: {avg_fde:.2f}m"
#     ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=14,
#             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9, edgecolor='black'))

#     ax.set_aspect('equal')
#     ax.legend(loc='upper right')
#     plt.title(f"Trajectory Prediction Visualization - Sample {sample_id}")
#     plt.tight_layout()
    
#     save_dir = "/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Visualization/plots/finetune_project_validation"
#     os.makedirs(save_dir, exist_ok=True)
#     plt.savefig(os.path.join(save_dir, f"scenario_{sample_id}_{scenario_id}.png"), dpi=150, bbox_inches='tight')
#     plt.close()


# %%
# ---------------------------------------------------------
# 3. MAP TRANSFORMATION & CREATION (FIXED INDENTATION & LOGIC)
# ---------------------------------------------------------
def convert_lane_type(type_str):
    """Convert MTR lane type to your LaneType enum."""
    type_map = {
        'TYPE_FREEWAY': LaneType.Driving,
        'TYPE_SURFACE_STREET': LaneType.Driving,
        'TYPE_BIKE_LANE': LaneType.Sidewalk,
    }
    return type_map.get(type_str, LaneType.Unknown)

def create_map_object(map_infos):
    """
    Transforms the raw map data by subtracting the center_xy offset across 
    all map polylines vectorially BEFORE building the map objects.
    """
    if 'all_polylines' not in map_infos:
        return Map(map_features=[], dynamic_states=None)
        
    # [TRANSFORM RAW MAP]: Vectorized translation alignment
    raw_polylines = map_infos['all_polylines'].copy()
    polylines = torch.from_numpy(raw_polylines)

    map_features = []
    
    # Deal with lanes
    for lane in map_infos.get('lane', []):
        start, end = lane['polyline_index']
        geometry = polylines[start:end]
        polyline = [MapPoint(x=float(p[0]), y=float(p[1])) for p in geometry]
        lane_object = Lane(road_id=lane['id'], lane_id=lane['id'], 
                           type=convert_lane_type(lane['type']), 
                           polyline=polyline, entry_lanes=None, exit_lanes=None, boundary=None)
        map_features.append(lane_object)
        
    # Deal with crosswalks
    for crosswalk in map_infos.get('crosswalk', []):
        start, end = crosswalk['polyline_index']
        geometry = polylines[start:end]
        polyline = [MapPoint(x=float(p[0]), y=float(p[1])) for p in geometry]
        crosswalk_object = Crosswalk(polygon=polyline, id=crosswalk['id'])
        map_features.append(crosswalk_object)
    
    # Deal with road lines
    for road_line in map_infos.get('road_line', []):
        start, end = road_line['polyline_index']
        geometry = polylines[start:end]
        polyline = [MapPoint(x=float(p[0]), y=float(p[1])) for p in geometry]
        roadline_object = RoadLine(id=road_line['id'], type=convert_lane_type(road_line['type']), polyline=polyline)
        map_features.append(roadline_object)
        
    return Map(map_features=map_features, dynamic_states=None)


# %%
# ---------------------------------------------------------
# 4. LOAD DATASET & PROCESS
# ---------------------------------------------------------
def get_testing_set(cfg_file):
    import sys
    sys.path.insert(0, '../')
    mtr_root = "/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Prediction/MTR"
    if mtr_root not in sys.path:
        sys.path.insert(0, mtr_root)
    from mtr.datasets import build_dataloader
    from mtr.config import cfg, cfg_from_yaml_file
    from mtr.utils import common_utils
    
    cfg_from_yaml_file(cfg_file, cfg)
    log_file = "/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Visualization/cpx_mtr_viz/log_file_finetune.txt"
    logger = common_utils.create_logger(log_file, rank=cfg.LOCAL_RANK)
    test_set, test_loader, sampler = build_dataloader(dataset_cfg=cfg.DATA_CONFIG, dist=False, batch_size=80, training=False, logger=logger)
    
    dataset_from_dataloader = test_loader.dataset
    return dataset_from_dataloader

cfg_file_path = '/data/robert/CP-X-Prediction/Intersection-Code/Intersection-MTR/Prediction/MTR/tools/cfgs/challenge/mtr-finetuning-full-map-testing-V2XPNP.yaml'
testing_set = get_testing_set(cfg_file=cfg_file_path)

# %%
# ---------------------------------------------------------
# 5. EXECUTION LOOP WITH MAP ALIGNMENT
# ---------------------------------------------------------
num_scenarios_to_plot = 20
vector_map_dict = {}

for i in range(min(num_scenarios_to_plot, len(test_results))):
    scenario_id = str(test_results[i][0]['scenario_id'])
    
    # Safely get map data
    if hasattr(testing_set, 'get_map_data_by_id'):
        raw_map_data = testing_set.get_map_data_by_id(scenario_id)
    elif hasattr(testing_set, 'scenario_id_to_index'):
        idx = testing_set.scenario_id_to_index.get(scenario_id)
        raw_map_data = testing_set.map_infos[idx] if idx is not None else {}
    else:
        raw_map_data = {}

    print(f"\n=== Processing Scenario {scenario_id} ===")
    
    # --- TRANSFORMING THE RAW MAP: CALCULATE OFFSET ---
    # Determine the center of the scene from the agent's t=10 position
    agent_x = test_results[i][0]['gt_trajs'][10][0]
    map_offset = np.array([0.0, 0.0])
    
    if 'all_polylines' in raw_map_data and len(raw_map_data['all_polylines']) > 0:
        map_x = raw_map_data['all_polylines'][0][0]
        
    # Create the transformed map
    if scenario_id not in vector_map_dict:
        vector_map_dict[scenario_id] = create_map_object(raw_map_data)
        
    vector_map = vector_map_dict[scenario_id]

    if vector_map is not None:
        print(f"Plotting all agents for scenario: {scenario_id} (Sample {i})")
        plot_traj_withmap_withheading_specific(sample_id=i, data=test_results, vector_map=vector_map, mode=6)
        print('----------------------------------------------------')