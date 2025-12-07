import scipy
import numpy as np
from scipy.signal import savgol_filter
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import nearest_points, unary_union

TTC_THRESHOLD = 1.5


def generate_movement_polygon(traj, length, width, yaw):
    # Function to get the corners of the rectangle for each trajectory point
    def get_corners(x, y, heading, length, width):
        dx = length / 2
        dy = width / 2
        
        # Rotate corners based on the heading
        corners = np.array([
            [dx, dy],
            [dx, -dy],
            [-dx, -dy],
            [-dx, dy]
        ])
        
        # Rotation matrix
        rotation_matrix = np.array([
            [np.cos(heading), -np.sin(heading)],
            [np.sin(heading), np.cos(heading)]
        ])
        
        rotated_corners = np.dot(corners, rotation_matrix.T)
        return rotated_corners + [x, y]

    rectangles = []
    for i in range(traj.shape[0]):
        corners = get_corners(traj[i, 0], traj[i, 1], yaw[i], length, width)
        rectangles.append(Polygon(corners))

    # Union all rectangles to form the movement polygon
    movement_polygon = unary_union(rectangles)
    
    return movement_polygon


def get_conflict_point(traj, polygon, min_dis=2000):
    conflict_timestep = 0
    conflict_point = Point(traj[0, 0], traj[0, 1])
    
    for i in range(traj.shape[0]):
        point = Point(traj[i, 0], traj[i, 1])
        _, bound_point = nearest_points(point, polygon)
        dis = point.distance(bound_point)

        if dis == 0 and min_dis > 0:
            conflict_point = bound_point
            break
        
        elif dis < min_dis:
            min_dis = dis
            conflict_point = bound_point #conflict point on the boundary of the overlap area
            conflict_timestep = i + 1

    return conflict_point, conflict_timestep


def calculate_ttc(traj1, traj2, conflict_point, v1, v2):
    rel_pos1 = [conflict_point.x, conflict_point.y] - traj1[:]
    rel_vel1 = v1
    rel_pos2 = [conflict_point.x, conflict_point.y] - traj2[:]
    rel_vel2 = v2
    norm_rel_vel_sq1 = np.linalg.norm(rel_vel1) ** 2

    ttc1 = np.dot(rel_pos1, rel_vel1) / (norm_rel_vel_sq1 + 1e-5)

    if ttc1 < 0 or np.abs(rel_pos1[0] / (1e-5 + rel_vel1[0])) > 7.5 \
        or np.abs(rel_pos1[1] / (1e-5 + rel_vel1[1])) > 7.5 \
        or np.abs(rel_pos2[0] / (1e-5 + rel_vel2[0])) > 2.5 \
        or np.abs(rel_pos2[1] / (1e-5 + rel_vel2[1])) > 2.5:
        ttc = np.inf

    else:
        ttc = ttc1

    return ttc


def check_conflict(ru1_traj, ru2_traj, ru1_size, ru2_size, ru1_subclass, ru2_subclass):
    # check if the two agents' paths overlap
    path_check, overlap_area = check_overlap(ru1_traj, ru2_traj, ru1_size, ru2_size)
    if not path_check:
        return False, None 

    # get conflict point and timestep
    conflict_point_a, conflict_step_a = get_conflict_point(ru1_traj, overlap_area)
    conflict_point_b, conflict_step_b = get_conflict_point(ru2_traj, overlap_area)

    if ru1_subclass == 'Passenger_Vehicle':
        conflict_point = conflict_point_a
        conflict_step = conflict_step_a
    else:
        conflict_point = conflict_point_b
        conflict_step = conflict_step_b

    # allow more timesteps to check for conflict
    for t in range(min(conflict_step, 5)):
        if (ru1_traj[t, 3:] == [0.0, 0.0]).all() or (ru2_traj[t, 3:] == [0.0, 0.0]).all(): # velocity is 0    
            continue

        ttc = calculate_ttc(ru1_traj[t, :2], ru2_traj[t, :2], conflict_point, ru1_traj[t, 3:], ru2_traj[t, 3:])
        
        if ttc < TTC_THRESHOLD:
            print(t)
            return True, ttc + t * 0.1
        
    return False, None
    

def check_overlap(ru1_traj, ru2_traj, ru1_size, ru2_size):
    ru1_polygon = generate_movement_polygon(ru1_traj[:, :2], ru1_size[0], ru1_size[1], ru1_traj[:, 2])
    ru2_polygon = generate_movement_polygon(ru2_traj[:, :2], ru2_size[0], ru2_size[1], ru2_traj[:, 2])
    overlap = ru1_polygon.intersects(ru2_polygon)
    overlap_area = ru1_polygon.intersection(ru2_polygon) if overlap else None
    
    return overlap, overlap_area


def post_process(traj):
    # smooth the trajectory
    x, y = traj[:, 0], traj[:, 1]
    x_smooth = savgol_filter(x, 21, 5)
    y_smooth = savgol_filter(y, 21, 5)
    traj = np.stack([x_smooth, y_smooth], axis=1)

    heading = np.zeros((traj.shape[0],))
    v_x = np.zeros((traj.shape[0],))
    v_y = np.zeros((traj.shape[0],))

    for i in range(traj.shape[0] - 1):
        heading[i] = np.arctan2(traj[i+1, 1] - traj[i, 1], (traj[i+1, 0] - traj[i, 0]) + 1e-5)
        v_x[i] = (traj[i+1, 0] - traj[i, 0]) / 0.1
        v_y[i] = (traj[i+1, 1] - traj[i, 1]) / 0.1
    
    heading[-1] = heading[-2]
    v_x[-1] = v_x[-2]
    v_y[-1] = v_y[-2]
    traj = np.stack([x_smooth, y_smooth, heading, v_x, v_y], axis=1)

    return traj


def calculate_conflict(prediction_results, objects):
    results = []

    # iterate through all pairs of agents
    for i in prediction_results.keys():
        for j in prediction_results.keys():
            if i == j: # same agent
                continue
      
            ru1_possible_trajs = prediction_results[i][0]
            ru2_possible_trajs = prediction_results[j][0]
            ru1_traj_scores = prediction_results[i][1]
            ru2_traj_scores = prediction_results[j][1]

            ru1_subclass = objects[i][0]
            ru2_subclass = objects[j][0]
            ru1_size = objects[i][1]
            ru2_size = objects[j][1]

            if 'Vehicle' in ru1_subclass:
                ru1_size = [5.4, 2.2]
            elif 'Bicycle' in ru1_subclass:
                ru1_size = [1.6, 1.2]
            else:
                ru1_size = [0.8, 0.8]

            if 'Vehicle' in ru2_subclass:
                ru2_size = [5.4, 2.2]
            elif 'Bicycle' in ru2_subclass:
                ru2_size = [1.6, 1.2]
            else:
                ru2_size = [0.8, 0.8]
                    
            # iterate through all possible trajectories
            for ru1_traj, ru1_score in zip(ru1_possible_trajs, ru1_traj_scores):
                for ru2_traj, ru2_score in zip(ru2_possible_trajs, ru2_traj_scores):
                    # ignore low scoring trajectories
                    if ru1_score < 0.1 or ru2_score < 0.1:
                        continue
                    
                    # check if the pair of agents are vehicle and dummy
                    if not( ('Dummy' in ru1_subclass and 'Vehicle' in ru2_subclass) or \
                        ('Dummy' in ru2_subclass and 'Vehicle' in ru1_subclass) ):
                        continue
                    
                    ru1_traj_p = post_process(ru1_traj)
                    ru2_traj_p = post_process(ru2_traj)

                    conflict, ttc = check_conflict(ru1_traj_p, ru2_traj_p, ru1_size, ru2_size, ru1_subclass, ru2_subclass)
                
                    if conflict:
                        results.append((ttc, ru1_subclass, ru2_subclass))
                        break

    # get the minimum ttc
    if len(results) == 0:
        return False, None, None, None
    else:
        ttc = np.min([r[0] for r in results])
        idx = np.argmin([r[0] for r in results])
        ru1_subclass = results[idx][1]
        ru2_subclass = results[idx][2]

        return True, ttc, ru1_subclass, ru2_subclass
                    

    