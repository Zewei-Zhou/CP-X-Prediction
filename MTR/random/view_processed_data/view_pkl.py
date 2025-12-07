import pickle
import os

# training_infos_path = "/data/dataset/CP-X/data/waymo/processed_scenarios_training_infos.pkl"
# validation_infos_path = "/data/dataset/CP-X/data/waymo/processed_scenarios_val_infos.pkl"

# training_infos_output = "/data/robert/CP-X-Prediction/MTR/random/view_processed_data/training_infos.txt"
# validation_infos_output = "/data/robert/CP-X-Prediction/MTR/random/view_processed_data/validation_infos.txt"

training_processed = "/data/dataset/CP-X/data/waymo/processed_scenarios_training"
validation_processed = "/data/dataset/CP-X/data/waymo/processed_scenarios_validation"

random_training_output = "/data/robert/CP-X-Prediction/MTR/random/view_processed_data/random_training.txt"
random_validation_output = "/data/robert/CP-X-Prediction/MTR/random/view_processed_data/random_validation.txt"


# with open(training_infos_path, "rb") as f, open(training_infos_output, "w") as w:
#     loaded = pickle.load(f)
#     w.write(str(loaded))
    
# with open(validation_infos_path, "rb") as f, open(validation_infos_output, "w") as w:
#     loaded = pickle.load(f)
#     w.write(str(loaded))

random_training = os.listdir(training_processed)[0]
training_path = os.path.join(training_processed, random_training)

with open(training_path, "rb") as f, open(random_training_output, "w") as w:
    loaded = pickle.load(f)
    w.write(str(loaded))

random_validation = os.listdir(validation_processed)[0]
validation_path = os.path.join(validation_processed, random_validation)

with open(validation_path, "rb") as f, open(random_validation_output, "w") as w:
    loaded = pickle.load(f)
    w.write(str(loaded))

    
    