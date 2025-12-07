import json
from collections import defaultdict
import matplotlib.pyplot as plt
import os
import csv

# Load the JSON data
input_file_path = '/Users/zewei/01_Projects/202405_Safety_challenge/validation_data/Run_315/Radars_Run_315_sensor1.json'

try:
    with open(input_file_path, 'r') as file:
        data = json.load(file)
except Exception as e:
    print("Error loading JSON data: {}".format(e))
    exit()

# Function to extract object information
def extract_object_info(data):
    object_info = defaultdict(list)

    for entry in data:
        try:
            if entry["topic"] == "sensor-traffic-objects/sensor1":
                timestamp = entry["payload"]["timestamp"]
                objects = entry["payload"]["objects"]
                for obj in objects:
                    obj_id = obj["id"]
                    position_facing = obj.get("position_facing", [None, None, None])
                    position_front = obj.get("position_front", [None, None, None])
                    speed = obj.get("speed", None)
                    object_info[obj_id].append({
                        "timestamp": timestamp,
                        "acceleration": obj.get("acceleration", None),
                        "class": obj.get("class", None),
                        "closest_lane": obj.get("closest_lane", None),
                        "heading": obj.get("heading", None),
                        "id": obj_id,
                        "length": obj.get("length", None),
                        "position_facing_x": position_facing[0],
                        "position_facing_y": position_facing[1],
                        "position_facing_z": position_facing[2],
                        "position_front_x": position_front[0],
                        "position_front_y": position_front[1],
                        "position_front_z": position_front[2],
                        "speed": speed,
                        "cycles_since_last_update": obj.get("tracking_status", {}).get("cycles_since_last_update", None),
                        "mileage": obj.get("tracking_status", {}).get("mileage", None),
                        "new_object": obj.get("tracking_status", {}).get("new_object", None),
                        "quality": obj.get("tracking_status", {}).get("quality", None),
                        "within_zone": obj.get("within_zone", [])
                    })
        except KeyError as e:
            print("KeyError: Missing key in entry - {}".format(e))
        except Exception as e:
            print("Error processing entry: {}".format(e))
    
    return object_info

# Extract object information
object_info = extract_object_info(data)

# Save the extracted information to CSV files
output_dir = '/Users/zewei/01_Projects/202405_Safety_challenge/validation_data/radar'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for obj_id, details in object_info.items():
    csv_file_path = os.path.join(output_dir, 'object_{}.csv'.format(obj_id))
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = [
            'timestamp', 'acceleration', 'class', 'closest_lane', 'heading', 'id', 'length',
            'position_facing_x', 'position_facing_y', 'position_facing_z',
            'position_front_x', 'position_front_y', 'position_front_z', 'speed',
            'cycles_since_last_update', 'mileage', 'new_object', 'quality', 'within_zone'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for detail in details:
            writer.writerow(detail)

print("Extracted object information saved to CSV files in {}".format(output_dir))

# Plot trajectories for all objects in one figure with unique colors
def plot_all_trajectories(object_info):
    plt.figure(figsize=(15, 10))
    valid_data_found = False
    for obj_id, positions in object_info.items():
        x = [pos['position_facing_x'] for pos in positions if pos['position_facing_x'] is not None]
        y = [pos['position_facing_y'] for pos in positions if pos['position_facing_y'] is not None]

        if not x or not y:
            print("No valid positions found for object ID {}".format(obj_id))
            continue

        valid_data_found = True
        plt.plot(x, y, marker='o', label='Object ID {}'.format(obj_id))

    if not valid_data_found:
        print("No valid data found to plot.")
        return

    plt.title("Trajectories of All Objects")
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.legend()
    plt.grid(True)
    plot_file_path = os.path.join('/Users/zewei/01_Projects/202405_Safety_challenge/validation_data/radar', 'all_trajectories.png')
    plt.savefig(plot_file_path)
    plt.close()
    print("All trajectories plot saved at {}".format(plot_file_path))

# Generate the combined plot for all objects
plot_all_trajectories(object_info)

# Save the extracted information to a JSON file as well
output_path = '/Users/zewei/01_Projects/202405_Safety_challenge/validation_data/radar/extracted_object_info.json'
try:
    with open(output_path, 'w') as outfile:
        json.dump(object_info, outfile, indent=4)
    print("Extracted object information saved to {}".format(output_path))
except Exception as e:
    print("Error saving extracted object information: {}".format(e))
