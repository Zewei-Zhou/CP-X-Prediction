import numpy as np
from scipy.optimize import minimize
from scipy.optimize import minimize_scalar

## trajectory smoothing
# smoothing parameters
degree = 5
# frequency of the data
time_disp = 0.1  # 10 Hz, hardcode rn


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
        smoothness = k1 * np.sum(fx3 ** 2 + fy3 ** 2) + k2 * np.sum(fx2 ** 2 + fy2 ** 2)

        # Define the closeness to original points for the segment
        segment_x_polyval = np.polyval(poly_x, s)
        segment_y_polyval = np.polyval(poly_y, s)
        original_distance = np.sum((segment_x_polyval - x_segment) ** 2 + (segment_y_polyval - y_segment) ** 2)

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
        return (x_poly - orig_x) ** 2 + (y_poly - orig_y) ** 2

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
        opt_coeffs_x, opt_coeffs_y = optimize_pair(x, y, 0, len(x), k1, k2, k3, points_per_segment)
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
        opt_coeffs_x, opt_coeffs_y = optimize_pair(x, y, start_index_1, end_index_2, k1, k2, k3, points_per_segment,
                                                   prev_end)
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
            closest_x, closest_y, optimal_s = closest_point_on_polynomial(opt_poly_x, opt_poly_y, orig_x, orig_y)
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


def wrap_angle(angle):
    return (angle + np.pi) % (2 * np.pi) - np.pi