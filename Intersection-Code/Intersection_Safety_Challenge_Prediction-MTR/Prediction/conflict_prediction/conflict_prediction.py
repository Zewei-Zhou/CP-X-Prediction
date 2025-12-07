import pickle
import numpy as np
from shapely.geometry import Polygon, Point, MultiPolygon
from shapely.ops import nearest_points, unary_union


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
        corners = get_corners(traj[i,0], traj[i,1], yaw[i,0], length[i,0], width[i,0])
        rectangles.append(Polygon(corners))

    # Union all rectangles to form the movement polygon
    movement_polygon = unary_union(rectangles)
    
    return movement_polygon


def get_conflict_point(traj, polygon, min_dis=2000):
    conflict_timestep = 0
    conflict_point = Point(traj[0,0], traj[0,1])
    
    for i in range(traj.shape[0]):
        if np.isnan(traj[i, 0]):
            continue

        point = Point(traj[i,0], traj[i,1])
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
    norm_rel_vel_sq1 = np.linalg.norm(rel_vel1)**2
    
    ttc1 = np.dot(rel_pos1, rel_vel1) / (norm_rel_vel_sq1 + 1e-5)

    if ttc1 < 0 \
    or np.abs(rel_pos1[0]/(1e-5+rel_vel1[0])) > 7.5 \
    or np.abs(rel_pos1[1]/(1e-5+rel_vel1[1])) > 7.5 \
    or np.abs(rel_pos2[0]/(1e-5+rel_vel2[0])) > 2.5 \
    or np.abs(rel_pos2[1]/(1e-5+rel_vel2[1])) > 2.5:
        
        ttc = np.inf

    else:
        
        ttc = ttc1

    return ttc
    
    
def conflict_prediction(trajs_data, subclass, timestep):
    """
    Args:
        trajs_data (num_object, fut_horizon, 10):
        subclass (num_object):
        timestep (fut_horizon):

    Returns:
        conflict_flag    0: no conflict, 1: conflict
        subclass[object_a], subclass[object_b]: which road user subclasses are involved in the conflict
        int(timestep[t]+ttc): the timestamp at which the conflict occurs
        ttc
    """
    
    conflict_flag = 0 
    ttc_thred = 1.5
        
    num_object = trajs_data.shape[0]
    fut_time = trajs_data.shape[1]
    
    # x, y coordinates
    traj = np.zeros((num_object, fut_time, 2)) 
    traj[:,:,:] = trajs_data[:,:,:2]

    # width, length
    width = np.zeros((num_object, fut_time, 1))
    width[:,:,:] = trajs_data[:,:,3:4]
    length = np.zeros((num_object, fut_time, 1))
    length[:,:,:] = trajs_data[:,:,4:5]

    # yaw
    yaw = np.zeros((num_object, fut_time, 1))
    yaw[:,:,:] = trajs_data[:,:,6:7]

    # velocity x, y
    vel = np.zeros((num_object, fut_time, 2))    
    vel[:,:,:] = trajs_data[:,:,7:9]
    
    # generate polygon
    polygon_list = []
    for i in range(num_object):
        movement_polygon = generate_movement_polygon(traj[i,:,:], width[i,:,:], length[i,:,:], yaw[i,:,:])
        polygon_list.append(movement_polygon)
    
    # identify path overlap
    overlap_pair_id = []
    overlap_area = []
    for i in range(num_object-1):
        for j in range(i+1, num_object):
            overlap = polygon_list[i].intersects(polygon_list[j])
            if overlap:
                overlap_area.append(polygon_list[i].intersection(polygon_list[j]))
                overlap_pair_id.append([i, j])
    
    # analyze overlap condition and calculate ttc            
    for i in range(len(overlap_pair_id)):
        
        object_a = overlap_pair_id[i][0]
        object_b = overlap_pair_id[i][1]
        
        if (subclass[object_a] == 'Passenger_Vehicle' and subclass[object_b] != 'Passenger_Vehicle') \
            or (subclass[object_a] != 'Passenger_Vehicle' and subclass[object_b] == 'Passenger_Vehicle'):

            conflict_point_a, conflict_timestep_a = get_conflict_point(traj[object_a,:,:], overlap_area[i])
            conflict_point_b, conflict_timestep_b = get_conflict_point(traj[object_b,:,:], overlap_area[i])
            
            if subclass[object_a] == 'Passenger_Vehicle':
                conflict_timestep = conflict_timestep_a
                conflict_point = conflict_point_a
            else:
                conflict_timestep = conflict_timestep_b
                conflict_point = conflict_point_b

            for t in range(min(conflict_timestep, fut_time-1)):
                if (traj[object_a,t,:] == [0.0, 0.0]).all() or (traj[object_b,t,:] == [0.0, 0.0]).all() \
                or (vel[object_a,t,:] == [0.0, 0.0]).all() or (vel[object_b,t,:] == [0.0, 0.0]).all(): #  # traj is nan or speed is 0    
                    continue
                
                else:
                    ttc = calculate_ttc(traj[object_a,t,:], traj[object_b,t,:], conflict_point, \
                                        vel[object_a,t,:], vel[object_b,t,:])
                    
                    if ttc <= ttc_thred:
                        conflict_flag = 1
                        break
            
        if conflict_flag == 1:
            break
    
    if conflict_flag == 0:
        return conflict_flag, None, None, None, None
    else:
        return conflict_flag, subclass[object_a], subclass[object_b], int(timestep[t]+ttc), ttc


if __name__ == '__main__':
    #trajs_data: (num_object, fut_horizon, 10)
    #subclass: (num_object)
    #timestep: (fut_horizon)

    # load final prediction results
    with open("../../Postprocessing/final_prediction.pkl", "rb") as f:
        data = pickle.load(f)

    trajs_data = data['trajs']
    subclass = data['subclass']
    timestep = data['timestep']

    conflict_flag, subclass_object_a, subclass_object_b, conflict_timestep, ttc = \
        conflict_prediction(trajs_data, subclass, timestep)    