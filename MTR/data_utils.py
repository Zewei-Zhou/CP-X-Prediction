import numpy as np
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar
from maps import *


## trajectory smoothing
# smoothing parameters 
degree = 5
# frequency of the data
time_disp = 0.1 # 10 Hz, hardcode rn


def get_object_keygroups(df):
    # Group columns in csv based on each item
    groups = {}
    current_group = []
    current_key = 'Timestamp'

    for col in df.columns:
        if 'xctr' in col:  # Assuming each group starts with 'xctr'
            if current_group:
                groups[current_key] = current_group
            
            current_key = col
            current_group = [col]
        else:
            current_group.append(col)

    # Add the last group
    if current_group:
        groups[current_key] = current_group
    
    groups.pop('Timestamp')

    return groups


# smooth 2 segments of the trajectory by optimization
def optimize_pair(x, y, start_index_1, end_index_2, k1, k2, k3, points_per_segment, prev_end=None):

    s1 = np.linspace(0, 1, end_index_2 - start_index_1)
    x_segment = x[start_index_1:end_index_2]
    y_segment = y[start_index_1:end_index_2]
    
    coeffs_x = np.polyfit(s1, x_segment, degree)
    coeffs_y = np.polyfit(s1, y_segment, degree)
    
    def objective(coeffs):
        # Extract the coefficients for x and y
        coeffs_x = coeffs[:degree + 1]
        coeffs_y = coeffs[degree + 1:]
        
        # Define polynomials for x and y
        poly_x = np.poly1d(coeffs_x)
        poly_y = np.poly1d(coeffs_y)
        
        # Define the smoothness objective (e.g., minimizing the integral of the square of the third derivative)
        s = np.linspace(0, 1, len(x_segment))
    
        # Calculate the third derivatives of the polynomials
        fx2 = np.polyder(poly_x, 2)(s)
        fy2 = np.polyder(poly_y, 2)(s)
        fx3 = np.polyder(poly_x, 3)(s)
        fy3 = np.polyder(poly_y, 3)(s)
        # Compute the smoothness criteria
        smoothness = k1 * np.sum(fx3**2 + fy3**2) + k2 * np.sum(fx2**2 + fy2**2)
        
        # Define the closeness to original points for the segment
        segment_x_polyval = np.polyval(poly_x, s)
        segment_y_polyval = np.polyval(poly_y, s)
        original_distance = np.sum((segment_x_polyval - x_segment)**2 + (segment_y_polyval - y_segment)**2)
        
        # Combine objectives with weighting factors
        return smoothness + k3 * original_distance  # The weighting factor can be adjusted
    
    initial_guess = np.hstack([coeffs_x, coeffs_y])
    constraints = []
    
    if prev_end is not None:
        def continuity_constraint(coeffs):
            coeffs_x = coeffs[:degree + 1]
            coeffs_y = coeffs[degree + 1:]
            poly_x = np.poly1d(coeffs_x)
            poly_y = np.poly1d(coeffs_y)
            return [
                poly_x(0) - prev_end[0],
                poly_y(0) - prev_end[1],
                np.polyder(poly_x, 1)(0) - prev_end[2],
                np.polyder(poly_y, 1)(0) - prev_end[3],
                np.polyder(poly_x, 2)(0) - prev_end[4],
                np.polyder(poly_y, 2)(0) - prev_end[5],
                # np.polyder(poly_y, 3)(0) - prev_end[6],
                # np.polyder(poly_y, 4)(0) - prev_end[7],
            ]
        constraints.append({'type': 'eq', 'fun': continuity_constraint})

    result = minimize(objective, initial_guess, constraints=constraints)
    
    opt_coeffs_x = result.x[:degree + 1]
    opt_coeffs_y = result.x[degree + 1:]

    return opt_coeffs_x, opt_coeffs_y


# Function to find the closest point on the polynomial to the original point (orig_x, orig_y)
def closest_point_on_polynomial(poly_x, poly_y, orig_x, orig_y):
    # Define the distance function to minimize
    def distance_function(s):
        # Calculate the x and y coordinates on the polynomial at parameter s
        x_poly = np.polyval(poly_x, s)
        y_poly = np.polyval(poly_y, s)
        # Calculate the squared Euclidean distance
        return (x_poly - orig_x)**2 + (y_poly - orig_y)**2

    # Minimize the distance function over the interval [0, 1]
    result = minimize_scalar(distance_function, bounds=(0, 1), method='bounded')

    # Optimal parameter s for the closest point
    optimal_s = result.x

    # Coordinates of the closest point on the polynomial
    closest_x = np.polyval(poly_x, optimal_s)
    closest_y = np.polyval(poly_y, optimal_s)
    
    return closest_x, closest_y, optimal_s


# Optimize the trajectory
def optimize_traj(x, y, k1, k2, k3, points_per_segment):
    '''
    return:
    x_coeff_list: list of coefficients of x polynomials
    y_coeff_list: list of coefficients of y polynomials
    closest_x_points: list of x coordinates of the closest points on the polynomials
    closest_y_points: list of y coordinates of the closest points on the polynomials
    derivatives_x: list of x derivatives at the closest points for heading calculation
    derivatives_y: list of y derivatives at the closest points for heading calculation
    '''
    n_points = len(x)
    num_segments = n_points // points_per_segment
    x_coeff_list = []
    y_coeff_list = []

    # Optimization of each pair of segments
    prev_end = None

    if len(x) < 8:
        return None
    
    closest_x_points = []
    closest_y_points = []
    derivatives_x = []
    derivatives_y = []

    if num_segments == 1 or num_segments == 0:
        opt_coeffs_x, opt_coeffs_y = optimize_pair(x, y, 0, len(x),k1,k2,k3,points_per_segment)
        x_coeff_list.append(opt_coeffs_x)
        y_coeff_list.append(opt_coeffs_y)
        opt_poly_x = np.poly1d(opt_coeffs_x)
        opt_poly_y = np.poly1d(opt_coeffs_y)

        for j in range(len(x)):
            orig_x = x[j]
            orig_y = y[j]
            closest_x, closest_y, optimal_s = closest_point_on_polynomial(opt_poly_x, opt_poly_y, orig_x, orig_y)
            closest_x_points.append(closest_x)
            closest_y_points.append(closest_y)
            derivatives_x.append(np.polyder(opt_poly_x, 1)(optimal_s))
            derivatives_y.append(np.polyder(opt_poly_y, 1)(optimal_s))

        return x_coeff_list, y_coeff_list, closest_x_points, closest_y_points, derivatives_x, derivatives_y

    optimal_s = None
    for i in range(num_segments - 1):
        start_index_1 = i * points_per_segment
        end_index_2 = (i + 2) * points_per_segment if i < num_segments - 2 else len(x)
        
        # Optimize the pair (segment i and segment i+1)
        # opt_coeffs_x, opt_coeffs_y, prev_end = optimize_pair(x, y, start_index_1, end_index_2, prev_end)
        opt_coeffs_x, opt_coeffs_y = optimize_pair(x, y, start_index_1, end_index_2,k1, k2, k3, points_per_segment, prev_end)
        x_coeff_list.append(opt_coeffs_x)
        y_coeff_list.append(opt_coeffs_y)

        # Define the polynomial functions for x and y
        opt_poly_x = np.poly1d(opt_coeffs_x)
        opt_poly_y = np.poly1d(opt_coeffs_y)

        # Find and record the closest points on the polynomial for the original points in this segment
        if end_index_2 == len(x):
            end_index = len(x)
        else:
            end_index = (i + 1) * points_per_segment
        for j in range(start_index_1, end_index):
            orig_x = x[j]
            orig_y = y[j]
            # get the closet point o the polynomial of the original point
            closest_x, closest_y,optimal_s = closest_point_on_polynomial(opt_poly_x, opt_poly_y, orig_x, orig_y)
            closest_x_points.append(closest_x)
            closest_y_points.append(closest_y)
            derivatives_x.append(np.polyder(opt_poly_x, 1)(optimal_s))
            derivatives_y.append(np.polyder(opt_poly_y, 1)(optimal_s))

        prev_end = [opt_poly_x(optimal_s),
                    opt_poly_y(optimal_s),
                    np.polyder(opt_poly_x, 1)(optimal_s),
                    np.polyder(opt_poly_y, 1)(optimal_s),
                    np.polyder(opt_poly_x, 2)(optimal_s),
                    np.polyder(opt_poly_y, 2)(optimal_s)]
        
    return x_coeff_list, y_coeff_list, closest_x_points, closest_y_points, derivatives_x, derivatives_y


def get_polyline_dir(polyline):
    polyline_dir = np.zeros((polyline.shape[0], 1))

    for i in range(polyline.shape[0]-1):
        dir_vec = polyline[i+1] - polyline[i]
        polyline_dir[i] = np.arctan2(dir_vec[1], dir_vec[0])

    polyline_dir[-1] = polyline_dir[-2]

    return polyline_dir


# def decode_map_features_from_proto(map_features):
#     polylines = []
#     map_infos = {}
#     points_per_segment = 10

#     for cur_data in map_features:
#         # center line and side walk
#         if isinstance(cur_data, Lane):
#             global_type = cur_data.type # 1: center line, 2: side walk
#             cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) 
#                                      for mappoint in cur_data.polyline], axis=0)
#             cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
#             cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1) # x, y, dir, type

#             # cut the polyline into multiple segments
#             if cur_polyline.shape[0] > points_per_segment:
#                 for i in range(0, cur_polyline.shape[0], points_per_segment):
#                     cur_polyline_segment = cur_polyline[i:i+points_per_segment]
#                     d = np.linalg.norm(cur_polyline_segment[:, 0:2], axis=-1)
#                     if np.max(d) > 50:
#                         continue

#                     if cur_polyline_segment.shape[0] < 5:
#                         continue
#                     elif cur_polyline_segment.shape[0] < points_per_segment:
#                         pl = np.zeros((points_per_segment-cur_polyline_segment.shape[0], cur_polyline_segment.shape[1]))
#                         cur_polyline_segment = np.concatenate((cur_polyline_segment, pl), axis=0)

#                     polylines.append(cur_polyline_segment)

#         # boundary
#         if isinstance(cur_data, Lane) and cur_data.type == 1:
#             global_type = 4
#             cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) for mappoint in cur_data.boundary], axis=0)
#             cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
#             cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
            
#             if cur_polyline.shape[0] > points_per_segment:
#                 for i in range(0, cur_polyline.shape[0], points_per_segment):
#                     cur_polyline_segment = cur_polyline[i:i+points_per_segment]
#                     d = np.linalg.norm(cur_polyline_segment[:, 0:2], axis=-1)
#                     if np.max(d) > 50:
#                         continue

#                     if cur_polyline_segment.shape[0] < 5:
#                         continue
#                     elif cur_polyline_segment.shape[0] < points_per_segment:
#                         pl = np.zeros((points_per_segment-cur_polyline_segment.shape[0], cur_polyline_segment.shape[1]))
#                         cur_polyline_segment = np.concatenate((cur_polyline_segment, pl), axis=0)

#                     polylines.append(cur_polyline_segment)

#         # crosswalk
#         if isinstance(cur_data, Crosswalk):
#             global_type = 3
#             cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) for mappoint in cur_data.polygon], axis=0)
#             cur_polyline = cur_polyline[1::2]
#             cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
#             cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
#             polylines.append(cur_polyline)
    
#     map_infos = np.array(polylines, dtype=np.float32)

#     return map_infos

# def decode_map_features_from_proto(map_features, points_per_segment=10):
#     """
#     Convert Map object to polyline format for processing.
    
#     Args:
#         map_features: List of map feature objects (Lane, Crosswalk, etc.)
#         points_per_segment: Number of points per polyline segment
    
#     Returns:
#         numpy array of polylines with shape (num_polylines, points_per_segment, features)
#     """
#     polylines = []
    
#     def get_polyline_dir(polyline):
#         """Calculate direction (heading) for each point in polyline."""
#         polyline_pre = np.roll(polyline, shift=1, axis=0)
#         polyline_pre[0] = polyline[0]
#         diff = polyline - polyline_pre
#         polyline_dir = np.arctan2(diff[:, 1], diff[:, 0])
#         return polyline_dir[:, np.newaxis]
    
#     for cur_data in map_features:
#         # Center line and side walk
#         if isinstance(cur_data, Lane):
#             global_type = cur_data.type.value
#             cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) 
#                                      for mappoint in cur_data.polyline], axis=0)
#             cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
#             cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
            
#             # Cut the polyline into segments
#             if cur_polyline.shape[0] > points_per_segment:
#                 for i in range(0, cur_polyline.shape[0], points_per_segment):
#                     cur_polyline_segment = cur_polyline[i:i+points_per_segment]
#                     d = np.linalg.norm(cur_polyline_segment[:, 0:2], axis=-1)
#                     if np.max(d) > 50:
#                         continue
                    
#                     if cur_polyline_segment.shape[0] < 5:
#                         continue
#                     elif cur_polyline_segment.shape[0] < points_per_segment:
#                         pl = np.zeros((points_per_segment-cur_polyline_segment.shape[0], cur_polyline_segment.shape[1]))
#                         cur_polyline_segment = np.concatenate((cur_polyline_segment, pl), axis=0)
                    
#                     polylines.append(cur_polyline_segment)
            
#             # Process boundary - ADD CHECK FOR EMPTY BOUNDARY
#             if cur_data.type == LaneType.Driving and len(cur_data.boundary) > 0:
#                 global_type = 4
#                 cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) 
#                                         for mappoint in cur_data.boundary], axis=0)
#                 cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
#                 cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
                
#                 if cur_polyline.shape[0] > points_per_segment:
#                     for i in range(0, cur_polyline.shape[0], points_per_segment):
#                         cur_polyline_segment = cur_polyline[i:i+points_per_segment]
#                         d = np.linalg.norm(cur_polyline_segment[:, 0:2], axis=-1)
#                         if np.max(d) > 50:
#                             continue
                        
#                         if cur_polyline_segment.shape[0] < 5:
#                             continue
#                         elif cur_polyline_segment.shape[0] < points_per_segment:
#                             pl = np.zeros((points_per_segment-cur_polyline_segment.shape[0], cur_polyline_segment.shape[1]))
#                             cur_polyline_segment = np.concatenate((cur_polyline_segment, pl), axis=0)
                        
#                         polylines.append(cur_polyline_segment)
        
#         # Crosswalk
#         if isinstance(cur_data, Crosswalk):
#             global_type = 3
#             cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) 
#                                     for mappoint in cur_data.polygon], axis=0)
#             if len(cur_polyline) > 1:  # ADD CHECK
#                 cur_polyline = cur_polyline[1::2]  # Sample every other point
#                 cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
#                 cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
#                 polylines.append(cur_polyline)
    
#     if len(polylines) == 0:
#         return np.array([], dtype=np.float32).reshape(0, points_per_segment, 4)
    
#     map_infos = np.array(polylines, dtype=np.float32)
#     return map_infos

def decode_map_features_from_proto(map_features, points_per_segment=10):
    """
    Convert Map object to polyline format for processing.
    
    Args:
        map_features: List of map feature objects (Lane, Crosswalk, etc.)
        points_per_segment: Number of points per polyline segment
    
    Returns:
        numpy array of polylines with shape (num_polylines, points_per_segment, features)
    """
    polylines = []
    
    def get_polyline_dir(polyline):
        """Calculate direction (heading) for each point in polyline."""
        polyline_pre = np.roll(polyline, shift=1, axis=0)
        polyline_pre[0] = polyline[0]
        diff = polyline - polyline_pre
        polyline_dir = np.arctan2(diff[:, 1], diff[:, 0])
        return polyline_dir[:, np.newaxis]
    
    for cur_data in map_features:
        # Center line and side walk
        if isinstance(cur_data, Lane):
            global_type = cur_data.type.value
            cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) 
                                     for mappoint in cur_data.polyline], axis=0)
            cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
            cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
            
            # Cut the polyline into segments
            if cur_polyline.shape[0] >= points_per_segment:
                for i in range(0, cur_polyline.shape[0], points_per_segment):
                    cur_polyline_segment = cur_polyline[i:i+points_per_segment]
                    
                    # Skip if distance check fails
                    d = np.linalg.norm(cur_polyline_segment[1:, 0:2] - cur_polyline_segment[:-1, 0:2], axis=-1)
                    if len(d) > 0 and np.max(d) > 50:
                        continue
                    
                    if cur_polyline_segment.shape[0] < 5:
                        continue
                    elif cur_polyline_segment.shape[0] < points_per_segment:
                        # Pad to points_per_segment
                        pl = np.zeros((points_per_segment - cur_polyline_segment.shape[0], cur_polyline_segment.shape[1]))
                        cur_polyline_segment = np.concatenate((cur_polyline_segment, pl), axis=0)
                    
                    polylines.append(cur_polyline_segment)
            
            # Process boundary - CHECK FOR EMPTY BOUNDARY
            if cur_data.type == LaneType.Driving and len(cur_data.boundary) > 0:
                global_type = 4
                cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) 
                                        for mappoint in cur_data.boundary], axis=0)
                cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
                cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
                
                if cur_polyline.shape[0] >= points_per_segment:
                    for i in range(0, cur_polyline.shape[0], points_per_segment):
                        cur_polyline_segment = cur_polyline[i:i+points_per_segment]
                        
                        # Skip if distance check fails
                        d = np.linalg.norm(cur_polyline_segment[1:, 0:2] - cur_polyline_segment[:-1, 0:2], axis=-1)
                        if len(d) > 0 and np.max(d) > 50:
                            continue
                        
                        if cur_polyline_segment.shape[0] < 5:
                            continue
                        elif cur_polyline_segment.shape[0] < points_per_segment:
                            # Pad to points_per_segment
                            pl = np.zeros((points_per_segment - cur_polyline_segment.shape[0], cur_polyline_segment.shape[1]))
                            cur_polyline_segment = np.concatenate((cur_polyline_segment, pl), axis=0)
                        
                        polylines.append(cur_polyline_segment)
        
        # Crosswalk
        if isinstance(cur_data, Crosswalk):
            global_type = 3
            polygon_points = [np.array([mappoint.x, mappoint.y, global_type]) for mappoint in cur_data.polygon]
            
            if len(polygon_points) > 1:  # CHECK FOR EMPTY
                cur_polyline = np.stack(polygon_points, axis=0)
                cur_polyline = cur_polyline[1::2]  # Sample every other point
                
                if cur_polyline.shape[0] >= 2:  # Need at least 2 points
                    cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
                    cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
                    
                    # Pad or truncate to points_per_segment
                    if cur_polyline.shape[0] < points_per_segment:
                        pl = np.zeros((points_per_segment - cur_polyline.shape[0], cur_polyline.shape[1]))
                        cur_polyline = np.concatenate((cur_polyline, pl), axis=0)
                    else:
                        cur_polyline = cur_polyline[:points_per_segment]
                    
                    polylines.append(cur_polyline)
    
    if len(polylines) == 0:
        return np.array([], dtype=np.float32).reshape(0, points_per_segment, 4)
    
    # Now all polylines should have the same shape
    map_infos = np.stack(polylines, axis=0)
    return map_infos

def transform_to_center_frame(center, objects, map_info):
    # transform the objects to the center frame
    x, y, h = center[0], center[1], center[2]
    transformed_objects = objects.copy()
    transformed_maps = map_info.copy()

    objects_x = (objects[:, :, 0] - x) * np.cos(-h) - (objects[:, :, 1] - y) * np.sin(-h)
    objects_y = (objects[:, :, 0] - x) * np.sin(-h) + (objects[:, :, 1] - y) * np.cos(-h)
    objects_h = wrap_angle(objects[:, :, 2] - h)
    objects_vx = objects[:, :, 3] * np.cos(-h) - objects[:, :, 4] * np.sin(-h)
    objects_vy = objects[:, :, 3] * np.sin(-h) + objects[:, :, 4] * np.cos(-h)

    transformed_objects[:, :, 0] = objects_x
    transformed_objects[:, :, 1] = objects_y
    transformed_objects[:, :, 2] = objects_h
    transformed_objects[:, :, 3] = objects_vx
    transformed_objects[:, :, 4] = objects_vy
    transformed_objects[objects==0] = 0

    maps_x = (map_info[:, :, 0] - x) * np.cos(-h) - (map_info[:, :, 1] - y) * np.sin(-h)
    maps_y = (map_info[:, :, 0] - x) * np.sin(-h) + (map_info[:, :, 1] - y) * np.cos(-h)
    maps_h = wrap_angle(map_info[:, :, 2] - h)
    transformed_maps[:, :, 0] = maps_x
    transformed_maps[:, :, 1] = maps_y
    transformed_maps[:, :, 2] = maps_h
    transformed_maps[map_info==0] = 0

    return transformed_objects, transformed_maps


def transform_to_center_frame_no_rotation(center, objects):
    # transform the objects to the center frame
    x, y, h = center[0], center[1], center[2]
    transformed_objects = objects.copy()

    objects_x = (objects[:, :, 0] - x) * np.cos(-h) - (objects[:, :, 1] - y) * np.sin(-h)
    objects_y = (objects[:, :, 0] - x) * np.sin(-h) + (objects[:, :, 1] - y) * np.cos(-h)
    transformed_objects[:, :, 0] = objects_x
    transformed_objects[:, :, 1] = objects_y
    transformed_objects[objects==0] = 0

    return transformed_objects


def wrap_angle(angle):
    return (angle + np.pi) % (2 * np.pi) - np.pi