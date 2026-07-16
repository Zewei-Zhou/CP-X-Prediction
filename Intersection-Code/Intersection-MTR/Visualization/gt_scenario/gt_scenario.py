import os
import numpy as np
import matplotlib.pyplot as plt
from Visualization.gt_scenario.data_preprocess import (create_infos_from_csv)

# load ground truth csv
# root_dirs = ['/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation',
#              '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/annotation2',
#              '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/validation_GT_second_release',
#              '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/perception_results',
#              '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/perception_results2']   # rehearsal_1
root_dirs = ['/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/rehearsal_3/group_d']
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

# draw the ground truth images
output_dir = '/Users/zewei/01_Projects/202405_Safety_challenge/Challenge_Prediction/Data/rehearsal_3/group_d/rehearsal_3_output'
os.makedirs(output_dir, exist_ok=True)

for scene in info_all.keys():
    trajs = info_all[scene]['trajs']
    plt.figure()
    fig, ax = plt.subplots(figsize=(10, 15), dpi=300)

    for i in range(trajs.shape[0]):
        object_type_subclass = info_all[scene]['object_type_subclass'][i]
        valid_trajs = np.array([trajs[i, j, :2] for j in range(trajs.shape[1]) if trajs[i, j, -1] > 0])

        start_point, = ax.plot(valid_trajs[0, 0], valid_trajs[0, 1],
                               marker='*', markersize=10, label=object_type_subclass)

        ax.plot(valid_trajs[:, 0], valid_trajs[:, 1],
                linewidth=2.5, alpha=.9, color=start_point.get_color())

    ax.legend(fontsize='large')
    plt.tight_layout()
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(f'Scene {scene}')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    output_file = os.path.join(output_dir, f'scene_{scene}.png')
    fig.savefig(output_file)
    plt.close(fig)


# draw the annotation subclass distribution
# subclass_count = {}
# for run_id, info in info_all.items():
#     for subclass in info['object_type_subclass']:
#         if subclass in subclass_count:
#             subclass_count[subclass] += 1
#         else:
#             subclass_count[subclass] = 1
#
# subclasses = list(subclass_count.keys())
# counts = list(subclass_count.values())
#
# plt.figure(figsize=(12, 8))
# bars = plt.barh(subclasses, counts, color='skyblue')
# plt.xlabel('Count')
# plt.ylabel('Subclass')
# plt.title('Distribution of Subclass')
#
# for bar in bars:
#     plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, str(bar.get_width()), va='center')
#
# plt.tight_layout()
# plt.show()

