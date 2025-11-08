import pickle as pkl
# training_processed = "/data/robert/CP-X-Prediction/MTR/data/training_processed/1a6ff76bf224d597_285_1.pkl"
# pkl_txt = "/data/robert/CP-X-Prediction/MTR/1a6ff76bf224d597_285_1.txt"
training_processed = "/data/tianhui/waymo/processed_scenarios_training/sample_1a0ab17d7b851095.pkl"
pkl_txt = "sample_1a0ab17d7b851095.txt"
with open(training_processed, "rb") as f:
    data = pkl.load(f)
print(data.keys())
# print(data['input_ids'].shape)
# print(data)
with open(pkl_txt, "w") as f:
    f.write(str(data))