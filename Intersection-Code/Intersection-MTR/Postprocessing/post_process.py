import numpy as np
import pickle
import sys
sys.path.append("../map")

from map import Map, Lane, LaneType
from utils import *
from shapely.geometry import LineString, Point, Polygon
import matplotlib.pyplot as plt

# define the object type subclass
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


# load vector map
with open("../map/vector_map.pkl", "rb") as f:
    vector_map = pickle.load(f)

# get the boundaries of the vector map
boundaries = []

for m in vector_map.map_features:
    if isinstance(m, Lane) and m.type == LaneType.Driving:
        boundary = np.array([(p.x, p.y) for p in m.boundary])
        boundaries.append(LineString(boundary))


# load neural network prediction results
with open("result.pkl", "rb") as f:
    model_prediction_result = pickle.load(f)

# data format:
# model_prediction_result[i]: list of dictionaries
# model_prediction_result[i][j]: dictionary containing the prediction results for a scene
# model_prediction_result[i][j]['scenario_id']: run timestep
# model_prediction_result[i][j]['pred_trajs']: numpy array of shape (M, T, 2) M is modality, T is time step
# model_prediction_result[i][j]['pred_scores']: numpy array of shape (M,)
# model_prediction_result[i][j]['object_type']: the subclass of the object


## TODO: load prediction results for dummy VRUs


# post-process prediction results
final_prediction = {} # scenario_id: {object_id: (trajectory, subclass)}
pred_trajs = []

for i in range(len(model_prediction_result)): # for each scenario
    scenario_id = str(model_prediction_result[i][0]['scenario_id'])
    final_prediction[scenario_id] = {} # object_id: (trajectory, subclass)

    for j in range(len(model_prediction_result[i])): # for each object
        prediction = model_prediction_result[i][j]['pred_trajs']
        prediction_scores = model_prediction_result[i][j]['pred_scores']
        object_class = str(model_prediction_result[i][j]['object_type'])
        object_id = int(model_prediction_result[i][j]['object_id'])
        per_object_prediction = []

        # check if the trajectory is off-road
        for k in range(prediction.shape[0]):
            trajectory = LineString(prediction[k]).buffer(1.0, cap_style='square')
            offroad = check_offroad(trajectory, object_class, boundaries)
            if offroad:
                continue

            per_object_prediction.append((prediction[k], prediction_scores[k]))

        if len(per_object_prediction) == 0:
            per_object_prediction = [(prediction[i], prediction_scores[i]) for i in range(prediction.shape[0])]

        # select the most likely trajectory
        max_score = -1
        best_trajectory = None

        for traj, score in per_object_prediction:
            if score > max_score:
                max_score = score
                best_trajectory = traj

        best_trajectory = smooth_trajectory(best_trajectory, order=3, window_length=41)
        # length, width, height = object_dimension

        velocity = velocity_calculation(best_trajectory)
        yaw = yaw_calculation(best_trajectory)

        best_trajectory = np.concatenate((best_trajectory, velocity, yaw), axis=1)
        final_prediction[scenario_id][object_id] = (best_trajectory, object_class)

    # plot the prediction results
    if True:
        for m in vector_map.map_features:
            if isinstance(m, Lane):
                plt.plot([p.x for p in m.polyline], [p.y for p in m.polyline], 'k')

        for obj_id, (traj, obj_class) in final_prediction[scenario_id].items():
            # vary the color based on the speed profile
            speed = np.linalg.norm(traj[:, 2:4], axis=1)
            color = np.clip(speed / 10, 0, 1)
            color = plt.cm.jet(color)
            color = tuple([(float(c[0]), float(c[1]), float(c[2]), float(c[3])) for c in color])
            plt.scatter(traj[:, 0], traj[:, 1], c=color)

            # start and end points
            plt.scatter(traj[0][0], traj[0][1], c='r') # start point
            plt.scatter(traj[-1][0], traj[-1][1], c='g') # end point
            # heading arrow
            plt.arrow(traj[0][0], traj[0][1], 0.5*np.cos(traj[0][-1]), 0.5*np.sin(traj[0][-1]), 
                      head_width=0.2, head_length=0.2, fc='r', ec='r')

        plt.xlim(-40, 40)
        plt.ylim(-40, 40)
        plt.colorbar()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

# save the final prediction results
with open("final_prediction.pkl", "wb") as f:
    pickle.dump(final_prediction, f)