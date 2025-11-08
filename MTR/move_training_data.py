import os
import shutil
import random
from pathlib import Path
from collections import defaultdict

# Paths
train_dir = Path("/data/dataset/CP-X-Prediction/Waymo/training_processed")
val_dir = Path("/data/dataset/CP-X-Prediction/Waymo/validation_processed")

# 70% training, 15% testing and 15% validation data.
VAL_RATIO = 0.15
TEST_RATIO = 0.15


# Group files by scenario_id
scenario_files = defaultdict(list)
for file in train_dir.glob("*.pkl"):
    scenario_id = file.stem.split('_')[0]  # Extract scenario ID
    scenario_files[scenario_id].append(file)

print(f"Total scenarios: {len(scenario_files)}")
print(f"Total files: {sum(len(files) for files in scenario_files.values())}")

# Randomly select scenarios for validation
all_scenarios = list(scenario_files.keys())
random.shuffle(all_scenarios)

num_val_scenarios = int(len(all_scenarios) * VAL_RATIO)
num_test_scenarios = int(len(all_scenarios) * TEST_RATIO)
val_scenarios = all_scenarios[:num_val_scenarios]
# test_scenarios = all_scenarios[num_val_scenarios:num_val_scenarios + num_test_scenarios]

print(f"Moving {num_val_scenarios} scenarios to validation...")
# print(f"Moving {num_test_scenarios} scenarios to testing...")   

# Move files
moved_count_val = 0
for scenario_id in val_scenarios:
    for file in scenario_files[scenario_id]:
        shutil.move(str(file), str(val_dir / file.name))
        moved_count_val += 1
        
        if moved_count_val % 10000 == 0:
            print(f"Moved {moved_count_val} files...")

# moved_count_test = 0
# for scenario_id in test_scenarios:
#     for file in scenario_files[scenario_id]:
#         shutil.move(str(file), str(val_dir / file.name))  # Assuming test and val go to same dir
#         moved_count_test += 1
        
#         if moved_count_test % 10000 == 0:
#             print(f"Moved {moved_count_test} files...")

print(f"Done! Moved {moved_count_val} files to validation")
# print(f"Done! Moved {moved_count_test} files to testing")
print(f"Training: {len(list(train_dir.glob('*.pkl')))} files")
print(f"Validation: {len(list(val_dir.glob('*.pkl')))} files")
# print(f"Testing: {len(list(val_dir.glob('*.pkl')))} files")