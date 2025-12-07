"""
Enhanced QCNet-Style Waymo Visualization
Closely matches QCNet paper visualization with:
- Crosswalks as filled orange polygons
- Better road surface rendering
- Improved lane markings
- Polished visual appearance
"""

import pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch
from matplotlib.path import Path as MplPath
from matplotlib.collections import PolyCollection, LineCollection
from pathlib import Path
import argparse


def map_object_type(obj_type):
    """Map Waymo object type to integer"""
    if isinstance(obj_type, (int, np.integer)):
        return int(obj_type)
    if isinstance(obj_type, str):
        type_map = {
            'TYPE_UNSET': 0, 'TYPE_VEHICLE': 1, 'TYPE_PEDESTRIAN': 2,
            'TYPE_CYCLIST': 3, 'TYPE_OTHER': 4
        }
        return type_map.get(obj_type, 0)
    return 0


def load_waymo_data(pkl_path):
    """Load Waymo pickle file"""
    with open(pkl_path, 'rb') as f:
        data = pickle.load(f)
    
    track_infos = data['track_infos']
    map_infos = data['map_infos']
    current_time = data['current_time_index']
    tracks_to_predict = data['tracks_to_predict']
    
    trajs = track_infos['trajs']
    object_types = track_infos['object_type']
    
    # Get target
    target_idx = tracks_to_predict['track_index'][0]
    
    return {
        'trajs': trajs,
        'object_types': object_types,
        'map_infos': map_infos,
        'current_time': current_time,
        'target_idx': target_idx,
        'scenario_id': data.get('scenario_id', 'unknown'),
    }


def filter_nearby_agents(trajs, target_idx, current_time, radius=80, max_agents=20):
    """Filter to nearby agents"""
    target_pos = trajs[target_idx, current_time, :2]
    
    distances = []
    for i in range(len(trajs)):
        pos = trajs[i, current_time, :2]
        valid = trajs[i, current_time, 9] > 0
        
        if valid:
            dist = np.linalg.norm(pos - target_pos)
            distances.append((i, dist))
        else:
            distances.append((i, np.inf))
    
    distances.sort(key=lambda x: x[1])
    nearby = [target_idx] + [idx for idx, d in distances if idx != target_idx and d < radius]
    
    return nearby[:max_agents]


def extract_polyline_coords(poly_data):
    """Extract x, y coordinates from polyline data"""
    if not isinstance(poly_data, np.ndarray) or len(poly_data) == 0:
        return None, None
    
    try:
        if poly_data.ndim == 1:
            if len(poly_data) < 7:
                return None, None
            return np.array([poly_data[0]]), np.array([poly_data[1]])
        else:
            if len(poly_data) < 2 or poly_data.shape[1] < 2:
                return None, None
            return poly_data[:, 0], poly_data[:, 1]
    except:
        return None, None


def get_polyline_from_indices(all_polylines, start_idx, end_idx):
    """Extract polyline segment from all_polylines array"""
    if start_idx < 0 or end_idx > len(all_polylines):
        return None, None
    
    segment = all_polylines[start_idx:end_idx]
    if len(segment) < 2:
        return None, None
    
    return segment[:, 0], segment[:, 1]


def in_bounds(xs, ys, xlim, ylim, buffer=100):
    """Check if polyline is within view bounds"""
    if xs is None or ys is None or len(xs) == 0:
        return False
    return not (xs.max() < xlim[0] - buffer or xs.min() > xlim[1] + buffer or
                ys.max() < ylim[0] - buffer or ys.min() > ylim[1] + buffer)


def render_enhanced_map(ax, map_infos, xlim, ylim):
    """
    Enhanced map rendering matching QCNet paper style:
    - Crosswalks as filled orange polygons
    - Lane surfaces as black polygons
    - Proper lane markings (dashed yellow)
    - Road edges (white)
    """
    all_polylines = map_infos.get('all_polylines', None)
    
    if all_polylines is None or len(all_polylines) == 0:
        print("  ⚠️  No map polylines available")
        ax.set_facecolor('#888888')
        return 0
    
    # Gray background like QCNet paper
    ax.set_facecolor('#A0A0A0')
    
    # Extract map elements with their polyline indices
    lanes = map_infos.get('lane', [])
    crosswalks = map_infos.get('crosswalk', [])
    road_lines = map_infos.get('road_line', [])
    road_edges = map_infos.get('road_edge', [])
    stop_signs = map_infos.get('stop_sign', [])
    
    count = 0
    
    # 1. Draw LANE SURFACES first (lowest layer) - dark black polygons
    print("  Rendering lanes...")
    for lane in lanes:
        if 'polyline_index' not in lane:
            continue
        
        start_idx, end_idx = lane['polyline_index']
        xs, ys = get_polyline_from_indices(all_polylines, start_idx, end_idx)
        
        if xs is None or not in_bounds(xs, ys, xlim, ylim):
            continue
        
        # Draw lane as thick black line for road surface
        ax.plot(xs, ys, color='#1A1A1A', linewidth=10, alpha=1.0,
               solid_capstyle='round', zorder=1)
        count += 1
    
    # 2. Draw CROSSWALKS as filled orange/brown polygons (like QCNet paper)
    print("  Rendering crosswalks...")
    for crosswalk in crosswalks:
        if 'polyline_index' not in crosswalk:
            continue
        
        start_idx, end_idx = crosswalk['polyline_index']
        xs, ys = get_polyline_from_indices(all_polylines, start_idx, end_idx)
        
        if xs is None or not in_bounds(xs, ys, xlim, ylim):
            continue
        
        if len(xs) >= 4:
            # Create filled polygon for crosswalk
            vertices = np.column_stack([xs, ys])
            poly = Polygon(vertices, facecolor='#CD853F', edgecolor='#8B4513',
                          linewidth=2, alpha=0.85, zorder=3)
            ax.add_patch(poly)
            count += 1
        else:
            # Fallback to thick line if not enough points for polygon
            ax.plot(xs, ys, color='#CD853F', linewidth=8, alpha=0.85,
                   solid_capstyle='round', zorder=3)
            count += 1
    
    # 3. Draw ROAD LINES (lane markings) - yellow dashed lines
    print("  Rendering lane markings...")
    for road_line in road_lines:
        if 'polyline_index' not in road_line:
            continue
        
        start_idx, end_idx = road_line['polyline_index']
        xs, ys = get_polyline_from_indices(all_polylines, start_idx, end_idx)
        
        if xs is None or not in_bounds(xs, ys, xlim, ylim):
            continue
        
        line_type = road_line.get('type', '')
        
        # Yellow dashed lines for lane markings
        if 'YELLOW' in line_type or 'SINGLE' in line_type:
            ax.plot(xs, ys, color='#FFFF00', linewidth=2, linestyle='--',
                   dashes=(10, 10), alpha=0.95, zorder=4, solid_capstyle='round')
        elif 'DOUBLE' in line_type:
            ax.plot(xs, ys, color='#FFFF00', linewidth=3, linestyle='-',
                   alpha=0.95, zorder=4, solid_capstyle='round')
        else:
            ax.plot(xs, ys, color='#FFFFFF', linewidth=1.5, linestyle='--',
                   dashes=(8, 8), alpha=0.8, zorder=4, solid_capstyle='round')
        count += 1
    
    # 4. Draw ROAD EDGES - white solid lines
    print("  Rendering road edges...")
    for road_edge in road_edges:
        if 'polyline_index' not in road_edge:
            continue
        
        start_idx, end_idx = road_edge['polyline_index']
        xs, ys = get_polyline_from_indices(all_polylines, start_idx, end_idx)
        
        if xs is None or not in_bounds(xs, ys, xlim, ylim):
            continue
        
        ax.plot(xs, ys, color='#FFFFFF', linewidth=2.5, alpha=0.95,
               zorder=4, solid_capstyle='round')
        count += 1
    
    # 5. Draw STOP SIGNS (optional - small circles)
    for stop_sign in stop_signs:
        if 'position' not in stop_sign:
            continue
        
        pos = stop_sign['position']
        if len(pos) >= 2:
            x, y = pos[0], pos[1]
            if xlim[0] <= x <= xlim[1] and ylim[0] <= y <= ylim[1]:
                ax.scatter(x, y, s=150, c='#FF0000', marker='o',
                          edgecolors='white', linewidths=2, zorder=5, alpha=0.9)
    
    print(f"  Map elements rendered: {count}")
    return count


def draw_vehicle_box(ax, x, y, heading, is_target=False, color=None):
    """
    Draw vehicle bounding box with orientation indicator
    """
    width, length = 2.0, 4.5
    
    # Vehicle corners
    corners = np.array([
        [-length/2, -width/2],
        [length/2, -width/2],
        [length/2, width/2],
        [-length/2, width/2]
    ])
    
    # Rotate by heading
    cos_h, sin_h = np.cos(heading), np.sin(heading)
    rot_matrix = np.array([[cos_h, -sin_h], [sin_h, cos_h]])
    rotated = corners @ rot_matrix.T
    rotated[:, 0] += x
    rotated[:, 1] += y
    
    if is_target:
        # Target vehicle: bright blue with thick black border
        poly = Polygon(rotated, facecolor='#4169E1', edgecolor='#000000',
                      linewidth=3.5, alpha=0.98, zorder=20)
        ax.add_patch(poly)
        
        # Yellow direction indicator arrow
        arrow_len = length * 0.6
        dx, dy = arrow_len * cos_h, arrow_len * sin_h
        arrow = FancyArrowPatch((x, y), (x + dx, y + dy),
                               arrowstyle='->', color='#FFD700',
                               linewidth=4, zorder=21,
                               mutation_scale=25)
        ax.add_patch(arrow)
    else:
        # Other vehicles: white/light gray
        if color is None:
            color = '#F5F5F5'
        poly = Polygon(rotated, facecolor=color, edgecolor='#666666',
                      linewidth=1.8, alpha=0.92, zorder=10)
        ax.add_patch(poly)
        
        # Subtle gray direction line
        line_len = length * 0.4
        dx, dy = line_len * cos_h, line_len * sin_h
        ax.plot([x, x + dx], [y, y + dy], color='#808080', linewidth=2.5,
               solid_capstyle='round', zorder=11, alpha=0.8)


def visualize_qcnet_enhanced(data, save_path=None, show_all_agents=True, max_agents=15):
    """
    Enhanced QCNet-style visualization matching paper figures
    """
    
    trajs = data['trajs']
    object_types = data['object_types']
    map_infos = data['map_infos']
    current_time = data['current_time']
    target_idx = data['target_idx']
    scenario_id = data['scenario_id']
    
    print(f"\n🎯 Target Agent: {target_idx}")
    
    # Get nearby agents
    if show_all_agents:
        agents = filter_nearby_agents(trajs, target_idx, current_time,
                                      radius=80, max_agents=max_agents)
    else:
        agents = [target_idx]
    
    # Ensure target is first
    if target_idx in agents:
        agents.remove(target_idx)
    agents = [target_idx] + agents
    
    print(f"  Rendering {len(agents)} agents")
    
    # Count agent types
    type_counts = {0: 0, 1: 0, 2: 0, 3: 0}
    for i in agents:
        t = map_object_type(object_types[i])
        type_counts[t] = type_counts.get(t, 0) + 1
    
    print(f"  Vehicles: {type_counts[0] + type_counts[1]}")
    print(f"  Pedestrians: {type_counts[2]}")
    print(f"  Cyclists: {type_counts[3]}")
    
    # Create figure
    fig = plt.figure(figsize=(20, 20), facecolor='white')
    ax = fig.add_subplot(111)
    
    # Title
    title = f'Waymo Trajectory Prediction: {scenario_id}'
    if type_counts[2] > 0 or type_counts[3] > 0:
        title += ' (Mixed Traffic)'
    fig.suptitle(title, fontsize=22, fontweight='bold', y=0.98)
    
    # Get view center from target
    target_traj = trajs[target_idx, :, :2]
    target_valid = trajs[target_idx, :, 9] > 0
    
    if target_valid[current_time]:
        cx, cy = target_traj[current_time]
    else:
        valid_idx = np.where(target_valid)[0]
        if len(valid_idx) > 0:
            cx, cy = target_traj[valid_idx[0]]
        else:
            cx, cy = 0, 0
    
    print(f"  View center: ({cx:.1f}, {cy:.1f})")
    
    # Set view bounds
    view_range = 80
    xlim = [cx - view_range, cx + view_range]
    ylim = [cy - view_range, cy + view_range]
    
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.set_aspect('equal')
    ax.grid(False)
    ax.set_xlabel('X (meters)', fontsize=16, fontweight='bold')
    ax.set_ylabel('Y (meters)', fontsize=16, fontweight='bold')
    
    # Render enhanced map
    print("  Rendering map...")
    map_count = render_enhanced_map(ax, map_infos, xlim, ylim)
    
    if map_count == 0:
        print("  ⚠️  WARNING: No map elements rendered!")
    
    # Draw OTHER agents first (background layer)
    print("  Drawing other agents...")
    for agent_idx in agents[1:]:
        obj_type = map_object_type(object_types[agent_idx])
        traj = trajs[agent_idx, :, :2]
        valid = trajs[agent_idx, :, 9] > 0
        heading = trajs[agent_idx, :, 5]
        
        if valid.sum() == 0:
            continue
        
        # History trajectory - light gray
        hist_valid = valid[:current_time+1]
        if hist_valid.sum() > 1:
            hist_traj = traj[:current_time+1][hist_valid]
            ax.plot(hist_traj[:, 0], hist_traj[:, 1],
                   color='#D3D3D3', linewidth=2, linestyle='-',
                   alpha=0.6, zorder=6, solid_capstyle='round')
        
        # Future trajectory - light pink dashed
        fut_valid = valid[current_time+1:]
        if fut_valid.sum() > 1:
            fut_traj = traj[current_time+1:][fut_valid]
            ax.plot(fut_traj[:, 0], fut_traj[:, 1],
                   color='#FFB6C1', linewidth=2, linestyle='--',
                   dashes=(8, 8), alpha=0.6, zorder=6, solid_capstyle='round')
        
        # Current position
        if valid[current_time]:
            x, y = traj[current_time]
            h = heading[current_time]
            
            if obj_type == 2:  # Pedestrian
                ax.scatter(x, y, s=200, c='#90EE90', marker='o',
                          edgecolors='black', linewidths=2.5, zorder=12, alpha=0.95)
            elif obj_type == 3:  # Cyclist
                ax.scatter(x, y, s=240, c='#FFB6C1', marker='D',
                          edgecolors='black', linewidths=2.5, zorder=12, alpha=0.95)
            else:  # Vehicle
                draw_vehicle_box(ax, x, y, h, is_target=False)
    
    # Draw TARGET agent last (top layer)
    print("  Drawing target agent...")
    target_type = map_object_type(object_types[target_idx])
    target_traj = trajs[target_idx, :, :2]
    target_valid = trajs[target_idx, :, 9] > 0
    target_heading = trajs[target_idx, :, 5]
    
    # Target history - thick white/light gray line
    hist_valid = target_valid[:current_time+1]
    if hist_valid.sum() > 1:
        hist = target_traj[:current_time+1][hist_valid]
        ax.plot(hist[:, 0], hist[:, 1],
               color='#FFFFFF', linewidth=4.5, linestyle='-',
               alpha=0.98, zorder=15, solid_capstyle='round',
               label='History (Past)')
        print(f"    History: {len(hist)} timesteps")
    
    # Target future - thick red/pink dashed line
    fut_valid = target_valid[current_time+1:]
    if fut_valid.sum() > 1:
        fut = target_traj[current_time+1:][fut_valid]
        ax.plot(fut[:, 0], fut[:, 1],
               color='#FF4444', linewidth=4.5, linestyle='--',
               dashes=(12, 6), alpha=0.98, zorder=15, solid_capstyle='round',
               label='Future (Ground Truth)')
        print(f"    Future: {len(fut)} timesteps")
    
    # Target current position
    if target_valid[current_time]:
        x, y = target_traj[current_time]
        h = target_heading[current_time]
        
        print(f"    Current position: ({x:.1f}, {y:.1f}), heading: {h:.2f}")
        
        if target_type == 2:  # Pedestrian
            ax.scatter(x, y, s=450, c='#00FF00', marker='o',
                      edgecolors='black', linewidths=4, zorder=22, alpha=0.98,
                      label='Target Agent')
        elif target_type == 3:  # Cyclist
            ax.scatter(x, y, s=500, c='#FF1493', marker='D',
                      edgecolors='black', linewidths=4, zorder=22, alpha=0.98,
                      label='Target Agent')
        else:  # Vehicle
            draw_vehicle_box(ax, x, y, h, is_target=True)
    else:
        print("    ⚠️  Target not valid at current timestep!")
    
    # Enhanced legend
    legend_elements = [
        plt.Rectangle((0, 0), 1, 1, fc='#4169E1', ec='black', linewidth=2.5,
                     label='Target Agent'),
        plt.Rectangle((0, 0), 1, 1, fc='#F5F5F5', ec='#666666', linewidth=1.8,
                     label='Other Vehicles'),
    ]
    
    if type_counts[2] > 0:
        legend_elements.append(
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#00FF00',
                      markersize=14, markeredgecolor='black', markeredgewidth=2.5,
                      label='Pedestrians', linestyle='None')
        )
    
    if type_counts[3] > 0:
        legend_elements.append(
            plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#FF1493',
                      markersize=14, markeredgecolor='black', markeredgewidth=2.5,
                      label='Cyclists', linestyle='None')
        )
    
    legend_elements.extend([
        plt.Line2D([0], [0], color='#FFFFFF', linewidth=4, linestyle='-',
                  label='History (Past)'),
        plt.Line2D([0], [0], color='#FF4444', linewidth=4, linestyle='--',
                  label='Future (Ground Truth)'),
        plt.Rectangle((0, 0), 1, 1, fc='#1A1A1A', ec='none',
                     label='Road Surface'),
        plt.Line2D([0], [0], color='#FFFF00', linewidth=2.5, linestyle='--',
                  label='Lane Markings'),
        plt.Rectangle((0, 0), 1, 1, fc='#CD853F', ec='#8B4513', linewidth=1.5,
                     label='Crosswalks'),
        plt.Line2D([0], [0], color='#FFFFFF', linewidth=2.5,
                  label='Road Edges'),
    ])
    
    ax.legend(handles=legend_elements, loc='upper right', fontsize=14,
             framealpha=0.97, edgecolor='black', fancybox=True,
             shadow=True, borderpad=1)
    
    # Info box with scene statistics
    info_text = f"""Scene Info:
• Agents: {len(agents)}
• Vehicles: {type_counts[0] + type_counts[1]}
• Pedestrians: {type_counts[2]}
• Cyclists: {type_counts[3]}
• History: 11 steps (1.1s)
• Future: 80 steps (8.0s)"""
    
    ax.text(0.02, 0.98, info_text, transform=ax.transAxes,
           fontsize=13, va='top', family='monospace', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='white',
                    alpha=0.97, edgecolor='black', linewidth=2.5))
    
    plt.tight_layout()
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight',
                   facecolor='white', edgecolor='none')
        print(f"✅ Saved to: {save_path}")
    
    plt.close()
    return fig


def main():
    parser = argparse.ArgumentParser(
        description='Enhanced QCNet-Style Waymo Visualization'
    )
    parser.add_argument('--data_path', type=str,
                       default='/data/dataset/CP-X/data/waymo/processed_scenarios_training',
                       help='Path to directory containing .pkl files')
    parser.add_argument('--sample_idx', type=int, default=0,
                       help='Index of sample to visualize')
    parser.add_argument('--show_all_agents', action='store_true',
                       help='Show all nearby agents (not just target)')
    parser.add_argument('--max_agents', type=int, default=15,
                       help='Maximum number of agents to display')
    parser.add_argument('--save_path', type=str, default=None,
                       help='Output path for saved figure')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("ENHANCED QCNET-STYLE VISUALIZATION")
    print("=" * 80)
    
    # Load data
    data_dir = Path(args.data_path)
    pkl_files = sorted(list(data_dir.glob('*.pkl')))
    
    if not pkl_files:
        print(f"❌ No .pkl files found in {data_dir}")
        return
    
    print(f"\nFound {len(pkl_files)} scenario files")
    
    if args.sample_idx >= len(pkl_files):
        print(f"⚠️  Sample index {args.sample_idx} out of range, using 0")
        args.sample_idx = 0
    
    pkl_path = pkl_files[args.sample_idx]
    print(f"📂 Loading: {pkl_path.name}")
    
    # Load and visualize
    data = load_waymo_data(pkl_path)
    
    print("🎨 Generating visualization...")
    save_path = args.save_path or f'qcnet_enhanced_{args.sample_idx}.png'
    visualize_qcnet_enhanced(data, save_path, args.show_all_agents, args.max_agents)
    
    print("\n✅ Visualization complete!")
    print("=" * 80)


if __name__ == '__main__':
    main()