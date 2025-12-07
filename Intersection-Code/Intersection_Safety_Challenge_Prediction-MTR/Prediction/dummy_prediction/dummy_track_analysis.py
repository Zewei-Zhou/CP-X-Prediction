import numpy as np
import matplotlib.pyplot as plt
import copy
from sklearn.cluster import KMeans
import pickle


def dummy_track_analysis(info_all):
    dummy_end_points = {1: {34: [], 43: []},
                        2: {34: [], 43: []},
                        3: {12: [], 21: []},
                        4: {12: [], 21: []}}
    dummy_id = copy.deepcopy(dummy_end_points)
    avg_dummy_end_points = copy.deepcopy(dummy_end_points)
    dummy_start_points = copy.deepcopy(dummy_end_points)
    avg_dummy_start_points = copy.deepcopy(dummy_end_points)

    for scenario_id, info in info_all.items():
        object_classes = info['object_type_class']
        trajs = info['trajs']

        if 'Dummy' not in object_classes:
            continue
        dummy_index = object_classes.index('Dummy')
        dummy_traj = trajs[dummy_index]
        dummy_traj = dummy_traj[dummy_traj[:, -1] > 0]

        start_point = dummy_traj[0, :2]
        end_point = dummy_traj[-1, :2]

        # hard coding to detect the track position
        track_position = 0
        track_direction = 0
        if start_point[0] < 9 and start_point[1] < -12:
            track_position = 4
            track_direction = 12

        if end_point[0] < 9 and end_point[1] < -12:
            track_position = 4
            track_direction = 21

        if start_point[0] > 18 and start_point[1] > -1.5:
            track_position = 2
            track_direction = 34

        if end_point[0] > 18 and end_point[1] > -1.5:
            track_position = 2
            track_direction = 43

        if start_point[0] > 24 and start_point[1] > -21:
            track_position = 3
            track_direction = 21

        if end_point[0] > 24 and end_point[1] > -21:
            track_position = 3
            track_direction = 12

        if start_point[0] < 20 and start_point[1] < -21:
            track_position = 1
            track_direction = 43

        if end_point[0] < 20 and end_point[1] < -21:
            track_position = 1
            track_direction = 34

        dummy_end_points[track_position][track_direction].append(end_point)
        dummy_start_points[track_position][track_direction].append(start_point)
        dummy_id[track_position][track_direction].append(scenario_id)

    # hard coding to filter the collision end points
    dummy_end_points[3][12] = [point for point in dummy_end_points[3][12] if point[1] > -15]

    for position, directions in dummy_end_points.items():
        for direction, end_points in directions.items():
            if end_points:
                # Convert the list of points to a numpy array for easier calculations
                end_points_array = np.array(end_points)
                start_point_arry = np.array(dummy_start_points[position][direction])
                # Calculate the mean of all points along the x and y axes
                avg_dummy_end_points[position][direction] = \
                    [np.mean(end_points_array[:, 0]), np.mean(end_points_array[:, 1])]

                # hard coding, the 4 21 track has two start points
                if position == 4 and direction == 21:
                    kmeans = KMeans(n_clusters=2, random_state=0).fit(start_point_arry)
                    cluster_centers = kmeans.cluster_centers_
                    avg_dummy_start_points[position][direction] = [cluster_centers[0].tolist(),
                                                                   cluster_centers[1].tolist()]
                else:
                    avg_dummy_start_points[position][direction] = \
                        [[np.mean(start_point_arry[:, 0]), np.mean(start_point_arry[:, 1])]]
            else:
                avg_dummy_end_points[position][direction] = None  # If no points, set to None
                avg_dummy_start_points[position][direction] = None

    # Drawing the end points and average points
    # plot_dummy_tracks(dummy_end_points, dummy_start_points,
    #                   avg_dummy_end_points, avg_dummy_start_points)

    return avg_dummy_end_points, avg_dummy_start_points


def plot_dummy_tracks(dummy_end_points, dummy_start_points,
                      avg_dummy_end_points, avg_dummy_start_points):
    # Define colors for different directions within each position
    colors = {1: {34: 'red', 43: 'blue'},
              2: {34: 'green', 43: 'orange'},
              3: {12: 'purple', 21: 'brown'},
              4: {12: 'pink', 21: 'cyan'}}

    # Plot each track with respective colors
    fig, ax = plt.subplots()
    for position, directions in dummy_end_points.items():
        for direction, end_points_list in directions.items():
            for index, end_point in enumerate(end_points_list):
                x_end, y_end = end_point
                x_start, y_start = dummy_start_points[position][direction][index]

                color = colors[position][direction]

                ax.scatter(x_end, y_end, color=color, alpha=0.6)
                ax.scatter(x_start, y_start, color=color, alpha=0.6)

    # Plot the average end points using star markers
    for position, directions in avg_dummy_end_points.items():
        for direction, avg_end_points in directions.items():
            if avg_end_points:
                avg_x_end, avg_y_end = avg_end_points
                start_points = avg_dummy_start_points[position][direction]
                color = colors[position][direction]

            for avg_x_start, avg_y_start in start_points:
                ax.scatter(avg_x_start, avg_y_start, color=color, marker='*', s=200, edgecolor='black', alpha=0.8)

            ax.scatter(avg_x_end, avg_y_end, color=color, marker='*', s=200, edgecolor='black', alpha=0.8)

    ax.set_xlabel('X-coordinate')
    ax.set_ylabel('Y-coordinate')
    ax.set_title('Dummy Track Analysis')
    # ax.legend()
    plt.show()