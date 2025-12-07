import torch
import numpy as np
from tqdm import tqdm
from model_simple import MTR
from matplotlib import pyplot as plt
from train_utils import ChallengeDataset, batch_nms
from test_utils import *
from conflict import calculate_conflict

# Build model
device = torch.device('cpu')
model = MTR.load_from_checkpoint('/home/zhiyu/Projects/Project13/Predictor_v2/output/MTR_20240820211233/epoch=18.ckpt', 
                                 map_location=device)
model.eval()

# Build dataset
dataset = ChallengeDataset(['processed_scenarios/test_GT'])
test_set = ['214',  '410',  '1078',  '315',  '91', '48',  '179','448', '875', '363']

# Test metrics
ADE = []
FDE = []

# gather a single scenario
info = {}
for i in range(len(dataset)):
    data = dataset[i]
    meta_data = dataset.meta_data
    scenario_id = meta_data['scenario_id']
    if scenario_id not in info:
        info[scenario_id] = [i]
    else:
        info[scenario_id].append(i)


# Begin testing
for s in test_set:
    print(s)
    s_keys = [k for k in info.keys() if s in k.split('_')[0]]

    for t in tqdm(s_keys):
        indices = info[t]
        states = []
        results = []

        for i in indices:
            data = dataset[i]
            meta_data = dataset.meta_data
            inputs = {k: torch.tensor(v).unsqueeze(0).to(device) for k, v in data.items()}
            outputs = model(inputs)
        
            prediction_trajs = outputs['layer_3_trajs'].detach().cpu()
            prediction_scores = outputs['layer_3_scores'].detach().cpu().softmax(dim=1)
            #prediction_trajs, prediction_scores, _ = batch_nms(prediction_trajs, prediction_scores, num_ret_modes=2)
            prediction_trajs = prediction_trajs[0].numpy()
            prediction_scores = prediction_scores[0].numpy()
            #prediction_scores = prediction_scores / np.sum(prediction_scores)
            ground_truth = data['fut_gt_trajs'][0]
            ground_truth_valid = data['fut_valid'][0]

            #prediction_trajs = np.concatenate([prediction_trajs, ground_truth[None, :]], axis=0)

            state = meta_data['center_object_state']
            sub_class = meta_data['object_subclass']
            states.append((state, sub_class))

            global_prediction_trajs = transformer_to_global_frame(prediction_trajs, state)
            results.append((global_prediction_trajs, prediction_scores))

            error = np.linalg.norm(prediction_trajs[..., :2] - ground_truth[None, :], axis=-1)
            #print(error, prediction_scores)
            error = error * ground_truth_valid
            weighted_error = np.sum(error * prediction_scores[:, None], axis=0)
            #print(weighted_error)
            ADE.append(np.sum(weighted_error) / np.sum(ground_truth_valid))
            FDE.append(np.mean(weighted_error[-1])) if ground_truth_valid[-1] else None

        # Calculate conflict
        conflict, timestamp, ru1_subclass, ru2_subclass = calculate_conflict(results, states)
        if conflict:
            print("Conflict:", conflict, timestamp, ru1_subclass, ru2_subclass)
            #break

        '''
        # plot scene-level results
        plt.figure(figsize=(20, 20))
        plot_vector_map()

        colors = ['r', 'g', 'b', 'c', 'm']
        for i in range(len(results)):
            plot_agent(states[i][0], states[i][1], color=colors[i])
            plot_trajectory(results[i][0], color=colors[i])
            

        plt.gca().set_aspect('equal', adjustable='box')
        plt.tight_layout()
        plt.show()
        '''

# Print results
# Average Displacement Error
print("ADE:", np.mean(ADE))

# Final Displacement Error
print("FDE:", np.mean(FDE))
