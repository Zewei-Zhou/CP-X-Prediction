import numpy as np
import warnings
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar
from map import Lane, Crosswalk
from test_utils import get_prior_dummy_heading
# Object class
# object_type_subclass = {
#     0: 'Other',
#     1: 'Passenger_Vehicle',
#     2: 'Vehicle_Other',
#     3: 'VRU_Child',
#     4: 'VRU_Adult',
#     5: 'VRU_Adult_Using_Motorized_Bicycle', 
#     6: 'VRU_Adult_Using_Manual_Wheelchair',
#     7: 'VRU_Adult_Using_Motorized_Wheelchair',
#     8: 'VRU_Adult_Using_Cane',
#     9: 'VRU_Adult_Using_Stroller',
#     10: 'VRU_Adult_Using_Walker',
#     11: 'VRU_Adult_Using_Manual_Bicycle',
#     12: 'VRU_Adult_Using_Electric_Scooter',
#     13: 'VRU_Adult_Using_Manual_Scooter',
#     14: 'VRU_Adult_Using_Skateboard',
#     15: 'VRU_Adult_Using_Crutches',
#     16: 'VRU_Adult_Using_Cardboard_Box',
#     17: 'VRU_Adult_Using_Umbrella',
#     18: 'VRU_Adult_Dummy',
#     19: 'VRU_Child_Dummy',
#     20: 'VRU_Adult_Using_Motorized_Bicycle_Dummy',
#     21: 'VRU_Other',
# }

object_type_class = {
    0: 'Other',
    1: 'Passenger_Vehicle',
    2: 'Vehicle_Other',
    3: 'VRU_Child',
    4: 'VRU_Adult',
    5: 'VRU_Adult_Using_Wheelchair',
    6: 'VRU_Adult_Using_Bicycle',
    7: 'VRU_Adult_Using_Non-Motorized_Device/Prop_Other',
    8: 'VRU_Adult_Using_Scooter_or_Skateboard',
    9: 'VRU_Child_Dummy',
    10: 'VRU_Adult_Dummy',
    11: 'VRU_Adult_Using_Bicycle_Dummy',
    12: 'VRU_Other'
}

class_values = list(object_type_class.values())
subclass_values = list(object_type_class.values())

pedestrian_class = ['VRU_Child', 'VRU_Adult','VRU_Adult_Using_Wheelchair',\
                           'VRU_Adult_Using_Scooter_or_Skateboard', 'VRU_Other']
cyclist_class = ['VRU_Adult_Using_Non-Motorized_Device/Prop_Other','VRU_Adult_Using_Bicycle']
vehicle_class = ['Passenger_Vehicle', 'Vehicle_Other']
mapping_from_subclass_to_class = {
    'Other': 'Other',
    'Passenger_Vehicle': 'Passenger_Vehicle',
    'Vehicle_Other': 'Vehicle_Other',
    'VRU_Child': 'VRU_Child',
    'VRU_Adult': 'VRU_Adult',
    'VRU_Adult_Using_Motorized_Bicycle': 'VRU_Adult_Using_Bicycle',
    'VRU_Adult_Using_Manual_Wheelchair': 'VRU_Adult_Using_Wheelchair',
    'VRU_Adult_Using_Motorized_Wheelchair': 'VRU_Adult_Using_Wheelchair',
    'VRU_Adult_Using_Cane': 'VRU_Adult_Using_Non-Motorized_Device/Prop_Other',
    'VRU_Adult_Using_Stroller': 'VRU_Adult_Using_Non-Motorized_Device/Prop_Other',
    'VRU_Adult_Using_Walker': 'VRU_Adult_Using_Non-Motorized_Device/Prop_Other',
    'VRU_Adult_Using_Manual_Bicycle': 'VRU_Adult_Using_Bicycle',
    'VRU_Adult_Using_Electric_Scooter': 'VRU_Adult_Using_Scooter_or_Skateboard',
    'VRU_Adult_Using_Manual_Scooter': 'VRU_Adult_Using_Scooter_or_Skateboard',
    'VRU_Adult_Using_Skateboard': 'VRU_Adult_Using_Scooter_or_Skateboard',
    'VRU_Adult_Using_Crutches': 'VRU_Adult_Using_Non-Motorized_Device/Prop_Other',
    'VRU_Adult_Using_Cardboard_Box': 'VRU_Adult_Using_Non-Motorized_Device/Prop_Other',
    'VRU_Adult_Using_Umbrella': 'VRU_Adult_Using_Non-Motorized_Device/Prop_Other',
    'VRU_Child_Dummy': 'VRU_Child_Dummy',
    'VRU_Adult_Dummy': 'VRU_Adult_Dummy',
    'VRU_Adult_Using_Motorized_Bicycle_Dummy': 'VRU_Adult_Using_Bicycle_Dummy',
    'VRU_Other': 'VRU_Other',
}


# map class
map_class = {
    0: 'Other',
    1: 'Lane',
    2: 'SideWalk',
    3: 'CrossWalk',
    4: 'Boundary',
}


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


def decode_map_features_from_proto_qcnet(map_features):
    polylines = []
    map_infos = {}
    points_per_segment = 10

    for cur_data in map_features:
        # center line and side walk
        if isinstance(cur_data, Lane):
            global_type = cur_data.type # 1: center line, 2: side walk
            cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) 
                                     for mappoint in cur_data.polyline], axis=0)
            cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
            cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1) # x, y, dir, type

            # cut the polyline into multiple segments
            if cur_polyline.shape[0] > points_per_segment:
                for i in range(0, cur_polyline.shape[0], points_per_segment):
                    cur_polyline_segment = cur_polyline[i:i+points_per_segment]
                    d = np.linalg.norm(cur_polyline_segment[:, 0:2], axis=-1)
                    if np.max(d) > 50:
                        continue

                    if cur_polyline_segment.shape[0] < 5:
                        continue
                    elif cur_polyline_segment.shape[0] < points_per_segment:
                        pl = np.zeros((points_per_segment-cur_polyline_segment.shape[0], cur_polyline_segment.shape[1]))
                        cur_polyline_segment = np.concatenate((cur_polyline_segment, pl), axis=0)

                    polylines.append(cur_polyline_segment)

        # boundary
        if isinstance(cur_data, Lane) and cur_data.type == 1:
            global_type = 4
            cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) for mappoint in cur_data.boundary], axis=0)
            cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
            cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
            
            if cur_polyline.shape[0] > points_per_segment:
                for i in range(0, cur_polyline.shape[0], points_per_segment):
                    cur_polyline_segment = cur_polyline[i:i+points_per_segment]
                    d = np.linalg.norm(cur_polyline_segment[:, 0:2], axis=-1)
                    if np.max(d) > 50:
                        continue

                    if cur_polyline_segment.shape[0] < 5:
                        continue
                    elif cur_polyline_segment.shape[0] < points_per_segment:
                        pl = np.zeros((points_per_segment-cur_polyline_segment.shape[0], cur_polyline_segment.shape[1]))
                        cur_polyline_segment = np.concatenate((cur_polyline_segment, pl), axis=0)

                    polylines.append(cur_polyline_segment)

        # crosswalk
        if isinstance(cur_data, Crosswalk):
            global_type = 3
            cur_polyline = np.stack([np.array([mappoint.x, mappoint.y, global_type]) for mappoint in cur_data.polygon], axis=0)
            cur_polyline = cur_polyline[1::2]
            cur_polyline_dir = get_polyline_dir(cur_polyline[:, 0:2])
            cur_polyline = np.concatenate((cur_polyline[:, 0:2], cur_polyline_dir, cur_polyline[:, 2:]), axis=-1)
            polylines.append(cur_polyline)
    
    map_infos = np.array(polylines, dtype=np.float32)
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



object_type_subclass = {
    0: 'Other',
    1: 'Passenger_Vehicle',
    2: 'Vehicle_Other',
    3: 'VRU_Child',
    4: 'VRU_Adult',
    5: 'VRU_Adult_Using_Motorized_Bicycle', 
    6: 'VRU_Adult_Using_Manual_Wheelchair',
    7: 'VRU_Adult_Using_Motorized_Wheelchair',
    8: 'VRU_Adult_Using_Cane',
    9: 'VRU_Adult_Using_Stroller',
    10: 'VRU_Adult_Using_Walker',
    11: 'VRU_Adult_Using_Manual_Bicycle',
    12: 'VRU_Adult_Using_Electric_Scooter',
    13: 'VRU_Adult_Using_Manual_Scooter',
    14: 'VRU_Adult_Using_Skateboard',
    15: 'VRU_Adult_Using_Crutches',
    16: 'VRU_Adult_Using_Cardboard_Box',
    17: 'VRU_Adult_Using_Umbrella',
    18: 'VRU_Other'
}
object_type_class = {
    0: 'Other',
    1: 'Vehicle',
    2: 'VRU'
}
subclass_values = list(object_type_subclass.values())

# get traj info from csv
def decode_tracks_from_csv(df, object_id_start, csv_file=None, run_id=None):
    csv_keygroup = get_object_keygroups(df)
    track_infos = {
        'object_id': [],  
        'object_type_subclass': [],  
        'object_type_class': [],
        'object_type': [],  # {0: unset, 1: vehicle, 2: pedestrian, 3: cyclist, 4: others}
        'trajs': []
    }

    for key, group in csv_keygroup.items(): # retrieve each object
        # filter out the static vehicle
        if 'Vehicle_Other' in key:
            continue
        # get the state of the object at each timestamp
        # make sure key in order and key exists
        assert 'xctr' in group[0]
        assert 'yctr' in group[1]
        assert 'zctr' in group[2]
        assert 'xlen' in group[3]
        assert 'ylen' in group[4]
        assert 'zlen' in group[5]
        assert 'xrot' in group[6]
        assert 'yrot' in group[7]
        assert 'zrot' in group[8]

        xctr = df[group[0]].values
        yctr = df[group[1]].values
        zctr = df[group[2]].values
        xlen = df[group[3]].values
        ylen = df[group[4]].values
        zlen = df[group[5]].values
        zrot = df[group[8]].values

        # create valid token that is 1 when the vehicle has xyz value
        valid = np.ones(xctr.shape)
        valid[np.isnan(xctr) | np.isnan(yctr) | np.isnan(zctr)] = 0
        if valid.sum() == 0:
            continue

        dummy_flag = False
        if 'Dummy' in key:
            dummy_flag = True
            key_clean = key.replace('_Dummy', '')
        else:
            key_clean = key

        cur_subclass_clean = '_'.join(key_clean.split('_')[:-1])

        # get the type of the object for static and smoothing threshold and parameters
        # pedestrian_class = ['VRU_Child', 'VRU_Adult','VRU_Adult_Using_Manual_Wheelchair',\
        #                     'VRU_Adult_Using_Motorized_Wheelchair', 'VRU_Adult_Using_Cane', 'VRU_Adult_Using_Stroller',\
        #                     'VRU_Adult_Using_Walker', 'VRU_Adult_Using_Skateboard', 'VRU_Adult_Using_Crutches', 'VRU_Adult_Using_Cardboard_Box',\
        #                     'VRU_Adult_Using_Umbrella']
        # cyclist_class = ['VRU_Adult_Using_Motorized_Bicycle','VRU_Adult_Using_Manual_Bicycle',\
        #                 'VRU_Adult_Using_Electric_Scooter', 'VRU_Adult_Using_Manual_Scooter']
        # vehicle_class = ['Passenger_Vehicle', 'Vehicle_Other']
        pedestrian_class = ['VRU_Child', 'VRU_Adult','VRU_Adult_Using_Wheelchair',\
                           'VRU_Adult_Using_Scooter_or_Skateboard', 'VRU_Other']
        cyclist_class = ['VRU_Adult_Using_Non-Motorized_Device/Prop_Other','VRU_Adult_Using_Bicycle']
        vehicle_class = ['Passenger_Vehicle', 'Vehicle_Other']
        
        temp_type = 'Vehicle'
        if cur_subclass_clean in pedestrian_class:
            temp_type = 'Pedestrian'
        elif cur_subclass_clean in cyclist_class:
            temp_type = 'Cyclist'       

  
        if temp_type == 'Vehicle':
            static_threshold = 0.1
            k1 = 0.0001
            k2 = 0.0001
            k3 = 10
            degree = 5
            points_per_segment = 20
        
        elif temp_type == 'Pedestrian':
            static_threshold = 0.015
            k1 = 0.0001
            k2 = 0.0001
            k3 = 1
            points_per_segment = 40
        
        elif temp_type == 'Cyclist':
            static_threshold = 0.015
            k1 = 0.0001
            k2 = 0.0001
            k3 = 1
            points_per_segment = 40

        # filter out the static points
        valid_x = xctr[valid == 1]
        valid_y = yctr[valid == 1]
        dx = np.diff(valid_x)
        dy = np.diff(valid_y)
        static_mask = (np.abs(dx) <= static_threshold) & (np.abs(dy) <= static_threshold)
        static_start = static_mask[0]
        static_mask = np.concatenate(([static_start], static_mask))
        # Create a mask for non-static parts (static_mask is not True)
        non_static_mask = ~static_mask
        # Filter out the non-static points
        non_static_x = valid_x[non_static_mask]
        non_static_y = valid_y[non_static_mask]

        # optimize the non static points
        optimized_result = optimize_traj(non_static_x, non_static_y, k1,k2,k3,points_per_segment)
        
        # optimization failed since non static points are less than (8? need to check)
        if optimized_result is None:
            print('Optimization failed')
            # print(csv_file)
            # print(key)
            
            # plt.scatter(valid_x[static_mask], valid_y[static_mask], color='blue', label='Static Points')
            # plt.scatter(valid_x[non_static_mask], valid_y[non_static_mask], color='orange', label='Non-static Points')

            print("-------all static--------")
            valid_heading = np.zeros(valid_x.shape)
            # continue
            
            
        else:
            x_coeff_list, y_coeff_list,closest_x_points, closest_y_points, derivative_x, derivative_y = optimized_result
    
            optimized_valid_x = np.full(valid_x.shape, np.nan)
            optimized_valid_y = np.full(valid_y.shape, np.nan)
            optimized_valid_x[non_static_mask] = closest_x_points
            optimized_valid_y[non_static_mask] = closest_y_points

            valid_heading = np.full(valid_x.shape, np.nan)
            valid_heading[non_static_mask] = np.arctan2(derivative_y, derivative_x)


            # Fill in the static points (traj and heading), optimized_valid_x, optimized_valid_y unused now, might be deleted later
            static_indices = np.where(static_mask)[0]
            for i in static_indices:
                if i > 0:
                    # Find the last non-static point before the current static point
                    previous_non_static = i - 1
                    while previous_non_static >= 0 and static_mask[previous_non_static]:
                        previous_non_static -= 1
                    if previous_non_static >= 0:
                        optimized_valid_x[i] = optimized_valid_x[previous_non_static]
                        optimized_valid_y[i] = optimized_valid_y[previous_non_static]
                        valid_heading[i] = valid_heading[previous_non_static]

                if np.isnan(optimized_valid_x[i]):  # If no previous non-static point was found
                    # Use the next non-static point if the static point is at the start or no previous found
                    next_non_static = i + 1
                    while next_non_static < len(static_mask) and static_mask[next_non_static]:
                        next_non_static += 1
                    if next_non_static < len(static_mask):
                        optimized_valid_x[i] = optimized_valid_x[next_non_static]
                        optimized_valid_y[i] = optimized_valid_y[next_non_static]
                        valid_heading[i] = valid_heading[next_non_static]

        if 'Dummy' in key:
            valid_heading= get_prior_dummy_heading(run_id, valid_heading)

        # Calculate velocity 
        time_disp = 0.1
        velocity_x_valid = np.zeros(len(valid_x))
        velocity_y_valid = np.zeros(len(valid_y))

        # Compute velocities for all points except the first
        velocity_x_valid[1:] = valid_x[1:] - valid_x[:-1]
        velocity_y_valid[1:] = valid_y[1:] - valid_y[:-1]

        # Assign the velocity of the second point to the first point
        velocity_x_valid[0] = velocity_x_valid[1]
        velocity_y_valid[0] = velocity_y_valid[1]

        velocity_x_valid = velocity_x_valid/time_disp
        velocity_y_valid = velocity_y_valid/time_disp

        velocity_x = np.zeros(len(xctr))
        velocity_y = np.zeros(len(yctr))
        
        if velocity_x.ndim != 1 or valid.ndim != 1:
            breakpoint()

        velocity_x[valid == 1] = velocity_x_valid
        velocity_y[valid == 1] = velocity_y_valid
        

        headings = np.zeros(len(xctr))
        headings[valid == 1] = valid_heading

        cur_traj = np.stack([xctr, yctr, zctr, xlen, ylen, zlen, headings, velocity_x, velocity_y, valid], axis=1) # (num_timestamp, 10)



        # plt.plot(xctr[0], yctr[0], '*', color='yellow', markersize=10, label="Start Point")
        # plt.plot(xctr, yctr, 'o-', label="Original Path", color='orange', markersize=1)
        # plt.show()

        # plt.plot(headings)
        # plt.title("heading from derivative" + key)
        # plt.show()  



        # set object_id
        track_infos['object_id'].append(object_id_start)
        object_id_start += 1
        # Passenger_Vehicle_xctr
        # print(key)
        # set object_type_class
        if 'Dummy' in key:
            track_infos['object_type_class'].append('Dummy')
        elif 'Vehicle' in key:
            track_infos['object_type_class'].append('Vehicle')
        elif 'VRU' in key:
            track_infos['object_type_class'].append('VRU')
        else:
            print(key)
            exit()
            track_infos['object_type_class'].append('Other')
            warnings.warn(f"Warning: The key '{key}' does not contain 'Vehicle' or 'VRU'. Classified as 'Other'.")
        
        # set object_type_subclass
        cur_subclass = '_'.join(key.split('_')[:-1])

        if any(subclass in cur_subclass_clean for subclass in subclass_values[1:]):
            track_infos['object_type_subclass'].append(cur_subclass)
        else:
            track_infos['object_type_subclass'].append('Other')
            warnings.warn(f"Warning: The key '{key}' does not contain any of the predefined subclass. Classified as 'Other'.")
        

        if dummy_flag == True:
            track_infos['object_type'].append('TYPE_DUMMY')
        elif cur_subclass_clean in pedestrian_class:
            track_infos['object_type'].append('TYPE_PEDESTRIAN')
        elif cur_subclass_clean in cyclist_class:
            track_infos['object_type'].append('TYPE_CYCLIST')
        elif cur_subclass_clean in vehicle_class:
            track_infos['object_type'].append('TYPE_VEHICLE')
        else:
            print('?')
            print(cur_subclass)
            track_infos['object_type'].append('Other')


        track_infos['trajs'].append(cur_traj)

    track_infos['trajs'] = np.stack(track_infos['trajs'], axis=0)  # (num_objects, num_timestamp, 9)
    return track_infos, object_id_start


def create_info_single_prediction_scenario(info, total_track_infos, start_timestamp, map_infos, prediction_scenario_length = 91, cur_timestamp = 10):
    prediction_info = {}
    prediction_info['scenario_id'] = info['file_id'] + '_' + str(start_timestamp)
    prediction_info['timestamps_seconds'] = info['timestamps_seconds'][start_timestamp: start_timestamp + prediction_scenario_length] 
    # hard code current tine index
    prediction_info['current_time_index'] = cur_timestamp  #10
    
    # a track is considered "track_to_predict" is it is valid over the whole prediction interval
    track_valid = total_track_infos['trajs'][:, start_timestamp: start_timestamp + prediction_scenario_length, -1]
    track_valid_mask = np.all(track_valid != 0, axis=1)
    track_valid_indices = np.where(track_valid_mask)[0]


    if len(track_valid_indices) == 0:
        return None
    
    # note that track index is consistent in the same run file, but start from 0 in each file
    prediction_info['tracks_to_predict'] = {
        'track_index': track_valid_indices
    }

    prediction_info['tracks_to_predict']['object_type_subclass'] = [total_track_infos['object_type_subclass'][cur_idx] for cur_idx in prediction_info['tracks_to_predict']['track_index']]
    prediction_info['tracks_to_predict']['object_type_class'] = [total_track_infos['object_type_class'][cur_idx] for cur_idx in prediction_info['tracks_to_predict']['track_index']]
    prediction_info['tracks_to_predict']['object_type'] = [total_track_infos['object_type'][cur_idx] for cur_idx in prediction_info['tracks_to_predict']['track_index']]
    prediction_info['trajs'] = total_track_infos['trajs'][:, start_timestamp: start_timestamp + prediction_scenario_length, :]
    
    # Define the valid ranges for x and y
    # x_min, x_max = -30, 62
    # y_min, y_max = -70, 75
    # x_out_of_range = np.logical_or(prediction_info['trajs'][..., 0] < x_min, prediction_info['trajs'][..., 0] > x_max)
    # y_out_of_range = np.logical_or(prediction_info['trajs'][..., 1] < y_min, prediction_info['trajs'][..., 1] > y_max)
    # if np.any(x_out_of_range) or np.any(y_out_of_range):
    #     return None
  

    track_infos = {}
    track_infos['object_id'] = total_track_infos['object_id']
    track_infos['object_type_subclass'] = total_track_infos['object_type_subclass']
    track_infos['object_type_class'] = total_track_infos['object_type_class']   
    track_infos['object_type'] = total_track_infos['object_type']
    track_infos['trajs'] = total_track_infos['trajs'][:, start_timestamp: start_timestamp + prediction_scenario_length, :]
    prediction_info['track_infos'] = track_infos
    prediction_info['map_infos'] = map_infos

    return prediction_info
   
    

