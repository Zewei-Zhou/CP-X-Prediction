"""
Fixed Trajectory Prediction Visualization
Properly handles Waymo map polyline structure using polyline_index.
"""

import torch
import torch.nn.functional as F
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import argparse
import pickle
import glob
import random
import os

from model import MTR
from train_utils import load_config, TYPE_MAPPING


# ============== Color Scheme ==============
class Colors:
    # Map elements
    ROAD_EDGE = '#1A202C'        # Very dark for road boundaries
    ROAD_LINE_WHITE = '#718096'  # Gray for white lane markings
    ROAD_LINE_YELLOW = '#D69E2E' # Yellow for yellow markings
    CROSSWALK = '#ED8936'        # Orange for crosswalks
    LANE_CENTER = '#E2E8F0'      # Very light - usually hidden
    
    # Agents
    VEHICLE = '#2B6CB0'          # Blue for center vehicle
    VEHICLE_OTHER = '#63B3ED'    # Light blue for other vehicles
    PEDESTRIAN = '#E53E3E'       # Red for pedestrians
    CYCLIST = '#38A169'          # Green for cyclists
    
    # Trajectories - UNIFIED HISTORY COLOR
    HISTORY = '#4A5568'          # Darker gray for ALL agent histories (more visible)
    GT_FUTURE = '#48BB78'        # Green for ground truth
    PRED_FUTURE = '#805AD5'      # Purple for predictions
    
    # Highlights
    CENTER_HIGHLIGHT = '#ECC94B'  # Yellow highlight
    BACKGROUND = '#FFFFFF'
    GRID = '#EDF2F7'


class FixedVisualizer:
    """Visualizer that properly handles Waymo map structure."""
    
    def __init__(self, model=None, device='cuda'):
        self.model = model
        self.device = device
        if model:
            model.eval()
    
    def load_raw_scene(self, pkl_path):
        """Load raw scene data from pickle file."""
        with open(pkl_path, 'rb') as f:
            return pickle.load(f)
    
    def get_predictions(self, processed_sample):
        """Get model predictions from processed sample."""
        if self.model is None:
            return None, None
        
        batch = {}
        for k, v in processed_sample.items():
            if isinstance(v, np.ndarray):
                v = torch.from_numpy(v).float()
            batch[k] = v.unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            enc = self.model.encoder(batch)
            pred = self.model.predictor(enc)
            n_layers = self.model.cfg.get('decoder_layers', 4)
            trajs = pred[f'layer_{n_layers-1}_trajs'][0].cpu().numpy()
            scores = pred[f'layer_{n_layers-1}_scores'][0].cpu().numpy()
        
        return trajs, scores
    
    def transform_to_agent_frame(self, points, center_x, center_y, center_heading):
        """Transform points to agent-centric coordinate frame."""
        cos_h = np.cos(-center_heading)
        sin_h = np.sin(-center_heading)
        
        dx = points[:, 0] - center_x
        dy = points[:, 1] - center_y
        
        x_transformed = dx * cos_h - dy * sin_h
        y_transformed = dx * sin_h + dy * cos_h
        
        return np.column_stack([x_transformed, y_transformed])
    
    def draw_map_from_raw(self, ax, raw_data, center_x, center_y, center_heading, max_range=70):
        """Draw map properly using the raw data structure."""
        
        map_infos = raw_data['map_infos']
        all_polylines = map_infos['all_polylines']
        
        # ===== Draw Road Edges (most important - defines road boundary) =====
        for edge in map_infos.get('road_edge', []):
            start_idx, end_idx = edge['polyline_index']
            points = all_polylines[start_idx:end_idx, :2]
            
            # Transform to agent frame
            points_transformed = self.transform_to_agent_frame(
                points, center_x, center_y, center_heading
            )
            
            # Filter by range
            in_range = (np.abs(points_transformed[:, 0]) < max_range) & \
                       (np.abs(points_transformed[:, 1]) < max_range)
            if in_range.sum() < 2:
                continue
            
            # Find contiguous segments within range
            segments = self._get_contiguous_segments(points_transformed, in_range)
            
            for seg in segments:
                if len(seg) >= 2:
                    edge_type = edge.get('type', '')
                    linewidth = 2.5 if 'BOUNDARY' in edge_type else 2.0
                    ax.plot(seg[:, 0], seg[:, 1], 
                           color=Colors.ROAD_EDGE, 
                           linewidth=linewidth, 
                           alpha=0.9, 
                           zorder=3,
                           solid_capstyle='round')
        
        # ===== Draw Road Lines (lane markings) =====
        for line in map_infos.get('road_line', []):
            start_idx, end_idx = line['polyline_index']
            points = all_polylines[start_idx:end_idx, :2]
            
            points_transformed = self.transform_to_agent_frame(
                points, center_x, center_y, center_heading
            )
            
            in_range = (np.abs(points_transformed[:, 0]) < max_range) & \
                       (np.abs(points_transformed[:, 1]) < max_range)
            if in_range.sum() < 2:
                continue
            
            segments = self._get_contiguous_segments(points_transformed, in_range)
            
            line_type = line.get('type', '')
            
            # Determine style based on type
            if 'YELLOW' in line_type:
                color = Colors.ROAD_LINE_YELLOW
            else:
                color = Colors.ROAD_LINE_WHITE
            
            if 'BROKEN' in line_type:
                linestyle = (0, (5, 5))  # Dashed
                linewidth = 1.5
            else:
                linestyle = '-'
                linewidth = 1.8
            
            for seg in segments:
                if len(seg) >= 2:
                    ax.plot(seg[:, 0], seg[:, 1],
                           color=color,
                           linewidth=linewidth,
                           linestyle=linestyle,
                           alpha=0.7,
                           zorder=2,
                           solid_capstyle='round')
        
        # ===== Draw Crosswalks =====
        for cw in map_infos.get('crosswalk', []):
            start_idx, end_idx = cw['polyline_index']
            points = all_polylines[start_idx:end_idx, :2]
            
            points_transformed = self.transform_to_agent_frame(
                points, center_x, center_y, center_heading
            )
            
            # Check if any point is in range
            in_range = (np.abs(points_transformed[:, 0]) < max_range) & \
                       (np.abs(points_transformed[:, 1]) < max_range)
            if not in_range.any():
                continue
            
            # Draw crosswalk as polygon
            if len(points_transformed) >= 3:
                polygon = patches.Polygon(
                    points_transformed,
                    closed=True,
                    facecolor=Colors.CROSSWALK,
                    edgecolor=Colors.CROSSWALK,
                    alpha=0.3,
                    linewidth=2,
                    zorder=2
                )
                ax.add_patch(polygon)
    
    def _get_contiguous_segments(self, points, mask):
        """Split points into contiguous segments based on mask."""
        segments = []
        current_segment = []
        
        for i, (point, valid) in enumerate(zip(points, mask)):
            if valid:
                current_segment.append(point)
            else:
                if len(current_segment) >= 2:
                    segments.append(np.array(current_segment))
                current_segment = []
        
        if len(current_segment) >= 2:
            segments.append(np.array(current_segment))
        
        return segments
    
    def draw_vehicle(self, ax, x, y, heading, color, is_center=False):
        """Draw vehicle as rectangle."""
        length = 4.8 if is_center else 4.0
        width = 2.0 if is_center else 1.8
        alpha = 0.95 if is_center else 0.7
        
        rect = patches.FancyBboxPatch(
            (-length/2, -width/2), length, width,
            boxstyle="round,pad=0.05,rounding_size=0.3",
            linewidth=2.5 if is_center else 1.5,
            edgecolor='black' if is_center else '#333333',
            facecolor=color,
            alpha=alpha,
            zorder=20 if is_center else 15
        )
        
        transform = plt.matplotlib.transforms.Affine2D().rotate(heading).translate(x, y) + ax.transData
        rect.set_transform(transform)
        ax.add_patch(rect)
        
        # Windshield for center vehicle
        if is_center:
            ws_length, ws_width = length * 0.25, width * 0.7
            windshield = patches.FancyBboxPatch(
                (length/2 - ws_length - 0.2, -ws_width/2),
                ws_length, ws_width,
                boxstyle="round,pad=0.02",
                facecolor='#A8DADC',
                alpha=0.8,
                zorder=21
            )
            windshield.set_transform(transform)
            ax.add_patch(windshield)
    
    def draw_pedestrian(self, ax, x, y, color, is_center=False):
        """Draw pedestrian as circle."""
        radius = 0.7 if is_center else 0.6
        circle = plt.Circle((x, y), radius,
                            facecolor=color,
                            edgecolor='black' if is_center else '#333333',
                            linewidth=2.5 if is_center else 1.5,
                            alpha=0.95 if is_center else 0.8,
                            zorder=20 if is_center else 15)
        ax.add_patch(circle)
    
    def draw_cyclist(self, ax, x, y, heading, color, is_center=False):
        """Draw cyclist as small elongated rectangle."""
        length = 2.0 if is_center else 1.8
        width = 0.7 if is_center else 0.6
        rect = patches.FancyBboxPatch(
            (-length/2, -width/2), length, width,
            boxstyle="round,pad=0.05",
            linewidth=2.5 if is_center else 1.5,
            edgecolor='black' if is_center else '#333333',
            facecolor=color,
            alpha=0.95 if is_center else 0.8,
            zorder=20 if is_center else 15
        )
        transform = plt.matplotlib.transforms.Affine2D().rotate(heading).translate(x, y) + ax.transData
        rect.set_transform(transform)
        ax.add_patch(rect)
    
    def draw_trajectory(self, ax, traj, valid_mask, color, linewidth=2, 
                        alpha=0.8, linestyle='-', zorder=5, show_dots=False):
        """Draw trajectory."""
        valid_idx = np.where(valid_mask > 0.5)[0]
        if len(valid_idx) < 2:
            return
        
        valid_traj = traj[valid_idx]
        ax.plot(valid_traj[:, 0], valid_traj[:, 1],
                color=color, linewidth=linewidth, alpha=alpha,
                linestyle=linestyle, zorder=zorder,
                solid_capstyle='round')
        
        if show_dots:
            ax.scatter(valid_traj[::5, 0], valid_traj[::5, 1],
                      c=color, s=20, alpha=alpha*0.8, zorder=zorder+1)
    
    def visualize_from_raw(self, raw_data, processed_sample, predictions=None, 
                           pred_scores=None, figsize=(12, 12), max_range=70,
                           save_path=None, title=None):
        """Visualize scene using raw data for map and processed data for agents."""
        
        fig, ax = plt.subplots(figsize=figsize, facecolor='white')
        ax.set_facecolor(Colors.BACKGROUND)
        
        # Setup axis
        ax.set_xlim(-max_range, max_range)
        ax.set_ylim(-max_range, max_range)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3, linestyle='-', color=Colors.GRID, linewidth=0.5)
        ax.set_xlabel('X (meters)', fontsize=11)
        ax.set_ylabel('Y (meters)', fontsize=11)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        if title:
            ax.set_title(title, fontsize=14, fontweight='bold', pad=15)
        
        # Get center agent info for coordinate transform
        current_time_idx = raw_data['current_time_index']
        track_infos = raw_data['track_infos']
        tracks_to_predict = raw_data['tracks_to_predict']
        predict_indices = tracks_to_predict['track_index']
        
        if len(predict_indices) == 0:
            plt.close()
            return None, None
        
        # Get center agent state
        center_idx = predict_indices[0]
        center_traj = track_infos['trajs'][center_idx]
        center_state = center_traj[current_time_idx]
        center_x, center_y = center_state[0], center_state[1]
        center_heading = center_state[6]
        center_type = TYPE_MAPPING.get(track_infos['object_type'][center_idx], 1)
        
        # ===== Draw Map =====
        self.draw_map_from_raw(ax, raw_data, center_x, center_y, center_heading, max_range)
        
        # ===== Draw Agents from processed sample =====
        hist_trajs = processed_sample['hist_trajs']
        hist_valid = processed_sample['hist_valid']
        fut_gt_trajs = processed_sample['fut_gt_trajs']
        fut_valid = processed_sample['fut_valid']
        
        num_agents = hist_trajs.shape[0]
        
        # Collect all valid agents
        agents = []
        for i in range(num_agents):
            valid_idx = np.where(hist_valid[i] > 0.5)[0]
            if len(valid_idx) == 0:
                continue
            
            last_idx = valid_idx[-1]
            x, y = hist_trajs[i, last_idx, 0], hist_trajs[i, last_idx, 1]
            heading = hist_trajs[i, last_idx, 2]
            agent_type = int(hist_trajs[i, last_idx, 5])
            dist = np.sqrt(x**2 + y**2)
            
            # Skip if outside range
            if abs(x) > max_range or abs(y) > max_range:
                continue
            
            agents.append({
                'idx': i, 'x': x, 'y': y, 'heading': heading,
                'type': agent_type, 'dist': dist, 'is_center': i == 0
            })
        
        # Sort: center first, then by distance - show more agents now
        agents.sort(key=lambda a: (not a['is_center'], a['dist']))
        agents = agents[:15]  # Show up to 15 agents
        
        # ===== First pass: Draw ALL history trajectories (same color) =====
        for agent in agents:
            i = agent['idx']
            is_center = agent['is_center']
            
            # Draw history for all agents - same gray color
            # Use thicker lines and add dots to make history more visible
            linewidth = 3.0 if is_center else 2.0
            alpha = 0.85 if is_center else 0.6
            
            # Get valid history points
            valid_idx = np.where(hist_valid[i] > 0.5)[0]
            if len(valid_idx) >= 2:
                hist_points = hist_trajs[i, valid_idx, :2]
                
                # Draw the line
                ax.plot(hist_points[:, 0], hist_points[:, 1],
                       color=Colors.HISTORY, linewidth=linewidth, alpha=alpha,
                       zorder=5 if is_center else 4, solid_capstyle='round')
                
                # Add dots at each history point to make trajectory clearer
                dot_size = 25 if is_center else 12
                ax.scatter(hist_points[:-1, 0], hist_points[:-1, 1],  # Exclude last (current) point
                          c=Colors.HISTORY, s=dot_size, alpha=alpha * 0.8,
                          zorder=5 if is_center else 4, edgecolors='none')
        
        # ===== Second pass: Draw all agent shapes =====
        for agent in agents:
            i = agent['idx']
            x, y, heading = agent['x'], agent['y'], agent['heading']
            agent_type = agent['type']
            is_center = agent['is_center']
            
            # Draw highlight for center agent
            if is_center:
                highlight = plt.Circle((x, y), 5.0,
                                       facecolor='none',
                                       edgecolor=Colors.CENTER_HIGHLIGHT,
                                       linewidth=3, linestyle='--',
                                       alpha=0.9, zorder=19)
                ax.add_patch(highlight)
            
            # Draw agent shape based on type
            if agent_type == 1:  # Vehicle - rectangle
                color = Colors.VEHICLE if is_center else Colors.VEHICLE_OTHER
                self.draw_vehicle(ax, x, y, heading, color, is_center)
            elif agent_type == 2:  # Pedestrian - circle
                self.draw_pedestrian(ax, x, y, Colors.PEDESTRIAN, is_center)
            elif agent_type == 3:  # Cyclist - small rectangle
                self.draw_cyclist(ax, x, y, heading, Colors.CYCLIST, is_center)
            else:  # Unknown - circle
                self.draw_pedestrian(ax, x, y, '#888888', is_center)
        
        # ===== Draw ground truth future (center agent only) =====
        center_agent = next((a for a in agents if a['is_center']), None)
        if center_agent:
            i = center_agent['idx']
            self.draw_trajectory(ax, fut_gt_trajs[i], fut_valid[i],
                                Colors.GT_FUTURE, linewidth=4,
                                alpha=0.9, linestyle=(0, (5, 3)), zorder=10)
            
            # GT endpoint star
            fut_valid_idx = np.where(fut_valid[i] > 0.5)[0]
            if len(fut_valid_idx) > 0:
                end_idx = fut_valid_idx[-1]
                ax.scatter(fut_gt_trajs[i, end_idx, 0], fut_gt_trajs[i, end_idx, 1],
                          c=Colors.GT_FUTURE, s=250, marker='*',
                          edgecolors='white', linewidths=2, zorder=25)
        
        # ===== Draw Predictions =====
        if predictions is not None:
            if pred_scores is not None:
                probs = self._softmax(pred_scores)
                best_mode = np.argmax(probs)
            else:
                probs = np.ones(len(predictions)) / len(predictions)
                best_mode = 0
            
            # Draw best prediction
            pred_valid = np.ones(len(predictions[best_mode]))
            self.draw_trajectory(ax, predictions[best_mode], pred_valid,
                                Colors.PRED_FUTURE, linewidth=4.5,
                                alpha=0.95, zorder=12)
            
            # Prediction endpoint
            ax.scatter(predictions[best_mode, -1, 0], predictions[best_mode, -1, 1],
                      c=Colors.PRED_FUTURE, s=300, marker='D',
                      edgecolors='white', linewidths=3, zorder=26)
            
            # Probability label
            ax.annotate(f'p={probs[best_mode]:.2f}',
                       xy=(predictions[best_mode, -1, 0], predictions[best_mode, -1, 1]),
                       xytext=(12, 10), textcoords='offset points',
                       fontsize=11, fontweight='bold', color='white',
                       bbox=dict(boxstyle='round,pad=0.3', facecolor=Colors.PRED_FUTURE,
                                edgecolor='white', alpha=0.95))
        
        # ===== Legend =====
        legend_elements = [
            plt.Line2D([0], [0], color=Colors.HISTORY, linewidth=2, label='History (all agents)'),
            plt.Line2D([0], [0], color=Colors.GT_FUTURE, linewidth=3,
                      linestyle='--', label='Ground Truth'),
            plt.Line2D([0], [0], color=Colors.PRED_FUTURE, linewidth=4,
                      label='Prediction'),
            patches.Patch(facecolor=Colors.VEHICLE, edgecolor='black', label='Vehicle'),
            patches.Patch(facecolor=Colors.PEDESTRIAN, edgecolor='black', label='Pedestrian'),
            patches.Patch(facecolor=Colors.CYCLIST, edgecolor='black', label='Cyclist'),
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=9,
                 framealpha=0.95, edgecolor='#E2E8F0', ncol=2)
        
        # ===== Info Box =====
        type_names = {1: 'Vehicle', 2: 'Pedestrian', 3: 'Cyclist'}
        center_type_val = center_agent['type'] if center_agent else 1
        
        # Count valid history steps for center agent
        hist_steps = int(hist_valid[0].sum()) if len(hist_valid) > 0 else 0
        
        info_lines = [f"Target: {type_names.get(center_type_val, 'Unknown')}"]
        
        if predictions is not None and center_agent and fut_valid[center_agent['idx']].sum() > 0:
            pred_end = predictions[best_mode, -1]
            fut_valid_idx = np.where(fut_valid[center_agent['idx']] > 0.5)[0]
            if len(fut_valid_idx) > 0:
                gt_end = fut_gt_trajs[center_agent['idx'], fut_valid_idx[-1]]
                fde = np.linalg.norm(pred_end - gt_end)
                info_lines.append(f"FDE: {fde:.1f}m")
        
        info_text = '\n'.join(info_lines)
        
        ax.text(0.98, 0.02, info_text,
               transform=ax.transAxes, fontsize=11, fontweight='medium',
               verticalalignment='bottom', horizontalalignment='right',
               bbox=dict(boxstyle='round,pad=0.5', facecolor='white',
                        edgecolor='#E2E8F0', alpha=0.95))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight', facecolor='white')
            print(f"Saved: {save_path}")
        
        return fig, ax
    
    def _softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / exp_x.sum()


def visualize_scenes(model, data_path, cfg, device='cuda', num_scenes=6,
                     save_dir='visualizations_fixed', max_range=70, vehicles_only=True):
    """Visualize scenes with proper map rendering."""
    
    from train_utils import WaymoDataset
    
    os.makedirs(save_dir, exist_ok=True)
    
    viz = FixedVisualizer(model, device)
    
    # Get list of pkl files
    pkl_files = sorted(glob.glob(f"{data_path}/*.pkl"))
    print(f"Found {len(pkl_files)} scenes")
    
    # Create dataset for processed samples
    dataset = WaymoDataset(data_path, subset_fraction=0.1, random_seed=42)
    
    # Find vehicle-focused scenes if requested
    selected_indices = []
    random.seed(42)
    indices = list(range(len(dataset)))
    random.shuffle(indices)
    
    for idx in indices:
        if len(selected_indices) >= num_scenes:
            break
        
        sample = dataset[idx]
        hist_valid = sample['hist_valid']
        hist_trajs = sample['hist_trajs']
        
        valid_idx = np.where(hist_valid[0] > 0.5)[0]
        if len(valid_idx) == 0:
            continue
        
        agent_type = int(hist_trajs[0, valid_idx[-1], 5])
        
        if vehicles_only and agent_type != 1:
            continue
        
        selected_indices.append(idx)
    
    print(f"Selected {len(selected_indices)} {'vehicle' if vehicles_only else ''} scenes")
    
    # Visualize each scene
    for idx in selected_indices:
        # Get raw data
        pkl_file = dataset.data_list[idx]
        raw_data = viz.load_raw_scene(pkl_file)
        
        # Get processed sample
        processed_sample = dataset[idx]
        
        # Get predictions
        predictions, pred_scores = viz.get_predictions(processed_sample)
        
        # Visualize
        scene_id = os.path.basename(pkl_file).replace('.pkl', '').replace('sample_', '')
        save_path = os.path.join(save_dir, f'scene_{scene_id[:8]}.png')
        
        viz.visualize_from_raw(
            raw_data, processed_sample,
            predictions=predictions,
            pred_scores=pred_scores,
            max_range=max_range,
            save_path=save_path,
            title=f'Scene {scene_id[:8]}'
        )
        plt.close()
    
    print(f"\nSaved {len(selected_indices)} visualizations to {save_dir}")


def main():
    parser = argparse.ArgumentParser(description='Fixed trajectory visualization')
    parser.add_argument('--checkpoint', type=str, required=True)
    parser.add_argument('--cfg', type=str, required=True)
    parser.add_argument('--data_path', type=str, required=True)
    parser.add_argument('--num_scenes', type=int, default=6)
    parser.add_argument('--save_dir', type=str, default='visualizations_fixed')
    parser.add_argument('--max_range', type=float, default=70)
    parser.add_argument('--vehicles_only', action='store_true')
    args = parser.parse_args()
    
    # Load config
    cfg = load_config(args.cfg)
    if 'cfg' in cfg:
        cfg = cfg['cfg']
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    
    # Load model
    print(f"Loading: {args.checkpoint}")
    model = MTR.load_from_checkpoint(args.checkpoint, cfg=cfg)
    model = model.to(device).eval()
    
    # Visualize
    visualize_scenes(
        model, args.data_path, cfg, device,
        num_scenes=args.num_scenes,
        save_dir=args.save_dir,
        max_range=args.max_range,
        vehicles_only=args.vehicles_only
    )


if __name__ == '__main__':
    main()