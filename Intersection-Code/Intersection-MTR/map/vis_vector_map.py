import pickle
import os
import numpy as np
from map import *
from Visualization.gt_scenario.data_preprocess import create_infos_from_csv
from matplotlib import pyplot as plt

# load vector map
with open("vector_map.pkl", "rb") as f:
    vector_map = pickle.load(f)

# plot map features
fig, ax = plt.subplots()
fig.set_size_inches(20, 25)

legend_added = {}

# draw map (merged elements)
for feature in vector_map.map_features:
    if isinstance(feature, Lane):
        if feature.type == LaneType.Sidewalk:
            label = "Sidewalk" if "Sidewalk" not in legend_added else ""
            ax.plot([point.x for point in feature.polyline], [point.y for point in feature.polyline], 'k--',
                    linewidth=2, label=label)
            legend_added["Sidewalk"] = True
        elif feature.type == LaneType.Shoulder:
            # ax.plot([point.x for point in feature.polyline], [point.y for point in feature.polyline], 'k--',
            #       linewidth=2, label=f"shoulder-{feature.road_id}-{feature.lane_id}")
            continue
        else:
            label = "Lane" if "Lane" not in legend_added else ""
            ax.plot([point.x for point in feature.polyline], [point.y for point in feature.polyline], 'k',
                    label=label)
            legend_added["Lane"] = True
    elif isinstance(feature, Crosswalk):
        label = "Crosswalk" if "Crosswalk" not in legend_added else ""
        polygon = feature.polygon
        ax.plot([point.x for point in polygon], [point.y for point in polygon], 'k', linewidth=2,
                label=label)
        legend_added["Crosswalk"] = True
    elif isinstance(feature, RoadLine):
        label = "Road Line" if "Road Line" not in legend_added else ""
        ax.plot([point.x for point in feature.polyline], [point.y for point in feature.polyline], label=label)
        legend_added["Road Line"] = True
    elif isinstance(feature, WalkButton):
        label = "Walk Button" if "Walk Button" not in legend_added else ""
        ax.plot(feature.position.x, feature.position.y, "o", label=label)
        legend_added["Walk Button"] = True

# draw map (seperated elements)
# for index, feature in enumerate(vector_map.map_features):
#     if isinstance(feature, Lane):
#         polyline = [point.x for point in feature.polyline], [point.y for point in feature.polyline]
#         if feature.type == LaneType.Sidewalk:
#             line, = ax.plot(*polyline, '--', linewidth=2)
#             label = f"sidewalk-{feature.road_id}-{feature.lane_id}-{index}"
#         elif feature.type == LaneType.Shoulder:
#             line, = ax.plot(*polyline, '--', linewidth=2)
#             label = f"shoulder-{feature.road_id}-{feature.lane_id}-{index}"
#         else:
#             line, = ax.plot(*polyline)
#             label = f"lane-{feature.road_id}-{feature.lane_id}-{index}"
#         # Annotate the middle point of the polyline
#         mid_index = len(feature.polyline) // 2
#         mid_point = feature.polyline[mid_index]
#         ax.annotate(label, (mid_point.x, mid_point.y), textcoords="offset points", xytext=(0,10), ha='center')
#
#         if hasattr(feature, 'boundary'):
#             boundary_line = [point.x for point in feature.boundary], [point.y for point in feature.boundary]
#             ax.plot(*boundary_line)
#             boundary_mid_index = len(feature.boundary) // 5
#             boundary_mid_point = feature.boundary[boundary_mid_index]
#             # ax.annotate(f"{label}-boundary", (boundary_mid_point.x, boundary_mid_point.y), textcoords="offset points",
#             #             xytext=(0, 10), ha='center')
#
#     elif isinstance(feature, Crosswalk):
#         polygon = [point.x for point in feature.polygon], [point.y for point in feature.polygon]
#         line, = ax.plot(*polygon, linewidth=2)
#         label = f"crosswalk-{feature.id}"
#         # Annotate the middle point of the polygon
#         mid_index = len(feature.polygon) // 2
#         mid_point = feature.polygon[mid_index]
#         ax.annotate(label, (mid_point.x, mid_point.y), textcoords="offset points", xytext=(0,10), ha='center')
#     elif isinstance(feature, RoadLine):
#         polyline = [point.x for point in feature.polyline], [point.y for point in feature.polyline]
#         ax.plot(*polyline)
#     elif isinstance(feature, WalkButton):
#         ax.plot(feature.position.x, feature.position.y, "o")
#         ax.annotate(f"walk button-{feature.id}", (feature.position.x, feature.position.y), textcoords="offset points", xytext=(0,10), ha='center')

# ax.legend()
# plt.gca().set_aspect('equal', adjustable='box')
# plt.tight_layout()
# plt.show()


# plt trajectories
# load ground truth csv
root_dirs = ['/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation',
             '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation2',
             '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation3',
             '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/validation_GT_second_release']
             # '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/perception_results',
             # '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/perception_results2']
# root_dirs = ['/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation']
for index, root_dir in enumerate(root_dirs):
    if index == 0:
        csv_files = []
    csv_files += sorted([os.path.join(root_dir, x)
                         for x in os.listdir(root_dir) if
                         x.endswith('.csv')])

info_all = {}
object_id_start = 0
for csv_file in csv_files:
    info, object_id_start = create_infos_from_csv(csv_file, object_id_start)
    info_all.update({info['file_id']: info})

traj_color = {'Vehicle': [240 / 255, 147 / 255, 74 / 255],
              'Dummy': [176 / 255, 36 / 255, 24 / 255],
              'VRU': [115 / 255, 234 / 255, 163 / 255]}
for scene in info_all.keys():
    trajs = info_all[scene]['trajs']

    for i in range(trajs.shape[0]):
        object_type_class = info_all[scene]['object_type_class'][i]
        # if object_type_class == 'Dummy':
        valid_trajs = np.array([trajs[i, j, :2] for j in range(trajs.shape[1]) if trajs[i, j, -1] > 0])
        plt.plot(valid_trajs[:, 0], valid_trajs[:, 1],
                 color=traj_color[object_type_class], linewidth=2.5, alpha=.9,
                 label=object_type_class if object_type_class not in plt.gca().get_legend_handles_labels()[1] else "")

# the evaluation area
eval_area = [[-30, 62], [-50, 55]]
x_min, x_max = eval_area[0]
y_min, y_max = eval_area[1]
plt.plot([x_min, x_max, x_max, x_min, x_min], [y_min, y_min, y_max, y_max, y_min],
         linestyle='--', color=[46 / 255, 96 / 255, 143 / 255], linewidth=2.5,
         label='Evaluation Area')

plt.legend(fontsize='large')
plt.tight_layout()
plt.gca().set_aspect('equal', adjustable='box')
plt.show()
plt.savefig('vector_map.png')
